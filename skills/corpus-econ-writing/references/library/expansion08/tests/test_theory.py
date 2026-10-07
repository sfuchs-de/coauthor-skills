import importlib.util
import json
import math
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("theory08_test_edition", ROOT / "scripts/edition.py")
edition = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(edition)


class VocabularyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = edition.records()

    def check(self, text, suffix=".tex"):
        return edition.inspect(text, suffix, self.inventory)

    def test_supported_new_word(self):
        self.assertTrue(self.inventory["basket"]["status"].endswith("attested"))

    def test_abbreviation_does_not_license_currency(self):
        self.assertEqual(self.inventory["euro"]["status"], "other_pages_attested")
        value = self.check("Income is one euro.")
        self.assertFalse(value["lexical_gate_passed"])
        self.assertIn("euro", value["context_restrictions_used"])

    def test_new_word_evidence(self):
        with edition.sqlite3.connect(ROOT / "vocabulary/attested_vocabulary.sqlite") as db:
            self.assertTrue(db.execute("SELECT 1 FROM occurrences WHERE word='basket' AND paper_id LIKE 'TH%' LIMIT 1").fetchone())

    def test_labels(self):
        value = self.check("Assumption H holds. Study B explains income.")
        self.assertEqual([r["label"] for r in value["classified_labels"]], ["H","B"])
        self.assertTrue(value["lexical_gate_passed"])

    def test_tex_label(self):
        value = self.check(r"\textbf{Assumption~H} holds.")
        self.assertEqual(value["classified_labels"][0]["label"], "H")

    def test_label_offsets(self):
        text = "% Study B hidden\nAssumption H holds.\nStudy C explains income."
        value = self.check(text)
        self.assertEqual([r["line"] for r in value["classified_labels"]], [2,3])
        for row in value["classified_labels"]:
            self.assertEqual(text[row["start"]:row["end"]], row["label"])

    def test_arbitrary_symbol_not_exempt(self):
        self.assertFalse(self.check("H explains income.")["lexical_gate_passed"])

    def test_lowercase_label_not_exempt(self):
        self.assertFalse(self.check("Study b explains income.")["lexical_gate_passed"])

    def test_unknown_word_not_exempt(self):
        self.assertFalse(self.check("Study Z invents zzzzunattestedword.")["lexical_gate_passed"])

    def test_compound_not_exempt(self):
        value = self.check("feasible-direction")
        self.assertFalse(value["lexical_gate_passed"])
        self.assertTrue(value["compound_review_suggestions"])

    def test_hyphenated_label_not_exempt(self):
        value = self.check("Assumption H-income holds.")
        self.assertFalse(value["lexical_gate_passed"])
        self.assertFalse(value["classified_labels"])

    def test_possessive_label_not_exempt(self):
        self.assertFalse(self.check("Study B's income.")["classified_labels"])

    def test_math_stays_separate(self):
        self.assertTrue(self.check("Income changes. $zzzzunattestedword=1$")["lexical_gate_passed"])

    def test_no_new_approved_exceptions(self):
        policy = edition.load(edition.urban.BASE / "data/vocabulary_policy.json")
        self.assertFalse(edition.vocabulary.exceptions_from(policy))

    def test_inventory(self):
        self.assertEqual(len(edition.all_papers()), 59)
        self.assertEqual(len({p["id"] for p in edition.all_papers()}), 59)

    def test_duplicate_json_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "policy.json"
            path.write_text('{"exceptions":[],"exceptions":[]}')
            with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
                edition.load(path)

    def test_sample_audit_preserves_first_drafts(self):
        frozen = edition.load(ROOT / "evaluation/FIRST_AUDIT.json")
        for row in frozen["samples"]:
            self.assertEqual(edition.digest(ROOT / "evaluation/first" / (row["id"] + ".tex")), row["sha256"])

    def test_final_samples_match_receipt(self):
        frozen = edition.load(ROOT / "evaluation/RELEASE_AUDIT.json")
        self.assertEqual(frozen["lexical_passes"], 4)
        for row in frozen["samples"]:
            self.assertEqual(edition.digest(ROOT / "evaluation/final" / (row["id"] + ".tex")), row["sha256"])

    def test_frozen_protocol(self):
        receipt = edition.load(ROOT / "data/PRESERVATION_FREEZE.json")
        self.assertEqual(edition.digest(ROOT / "evaluation/PROTOCOL.md"), receipt["protocol_sha256"])

    def test_empty_draft(self):
        self.assertEqual(self.check("")["checked_tokens"], 0)


def derivative(function, point, step=1e-5):
    return (function(point+step)-function(point-step))/(2*step)


class DerivationTests(unittest.TestCase):
    def test_income_need_not_equal_expenditure_without_condition(self):
        # A household satiated at one unit can have income three, cost one.
        income, minimum_cost = 3, 1
        self.assertNotEqual(income, minimum_cost)
        self.assertNotEqual(minimum_cost/income, 1)

    def test_input_and_output_envelopes(self):
        p,r,a=1.7,0.9,1.3
        value=lambda p,r: (p*a)**2/(4*r)
        x=(p*a/(2*r))**2
        q=a*math.sqrt(x)
        self.assertAlmostEqual(derivative(lambda z:value(z,r),p),q,places=8)
        self.assertAlmostEqual(derivative(lambda z:value(p,z),r),-x,places=8)

    def test_marginal_not_average_share(self):
        # f(x)=sqrt(x)+1 makes the two shares different at p=r=1.
        q=1.5
        income=1.25
        price_share=q/(q+0.5)
        self.assertNotAlmostEqual(price_share,income/q)

    def test_input_adjustment_second_order(self):
        p,r,a=1.4,0.8,1.2
        x=(p*a/(2*r))**2
        gap=lambda h: ((p+h)*a)**2/(4*r)-((p+h)*a*math.sqrt(x)-r*x)
        self.assertAlmostEqual(gap(0.001)/gap(0.002),0.25,places=6)

    def test_total_policy_derivative(self):
        a,b,c,d,e,k,l,m,n=0.2,0.8,0.4,0.3,0.1,1.7,1.1,0.6,0.2
        t=0.7
        state=lambda z: ((a*d+b)*z+a*e*z*z)/(1-a*c)
        transfer=lambda z:c*state(z)+d*z+e*z*z
        welfare=lambda z:k*state(z)+l*transfer(z)+m*z+n*z*z
        Ep=(b+a*(d+2*e*t))/(1-a*c)
        total=m+2*n*t+l*(d+2*e*t)+(k+l*c)*Ep
        self.assertAlmostEqual(total,derivative(welfare,t),places=8)
        without_direct=l*(d+2*e*t)+(k+l*c)*Ep
        self.assertGreater(abs(without_direct-total),0.5)

    def test_transfer_value_experiment(self):
        a,b,k,l,t=0.3,0.8,1.7,1.1,0.7
        welfare=lambda T:k*(a*T+b*t)+l*T
        total=l+k*a
        self.assertAlmostEqual(total,derivative(welfare,0.4),places=8)
        self.assertNotAlmostEqual(total,l)

    def test_feedback_denominator_required(self):
        self.assertEqual(1-0.5*2,0)

    def test_income_share_correction(self):
        s=[0.2,0.3,0.5]
        slopes=[0,0.1,-0.05]
        sigma,g=2.4,0.07
        D=[(1-sigma)*z for z in slopes]
        bar=sum(a*b for a,b in zip(s,D))
        alpha=g-bar
        def log_spending(t,i):
            weights=[a*math.exp((1-sigma)*b*t) for a,b in zip(s,slopes)]
            return g*t+math.log(weights[i]/sum(weights))
        for i in range(3):
            self.assertAlmostEqual(derivative(lambda t:log_spending(t,i),0),alpha+D[i],places=8)
        self.assertAlmostEqual(alpha+bar,g,places=10)
        self.assertNotAlmostEqual(alpha,g)

    def test_nonsingular_not_convergent(self):
        coefficient=1.1
        self.assertNotEqual(1-coefficient,0)
        self.assertGreater(coefficient**100,100)

    def test_changing_feasibility_contributes(self):
        # max x subject to x<=t: the objective's direct t derivative is zero.
        self.assertAlmostEqual(derivative(lambda t:t,1.0),1,places=8)


if __name__ == "__main__":
    unittest.main()
