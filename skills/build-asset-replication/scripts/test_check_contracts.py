import copy
import json
import unittest
from pathlib import Path

from check_contracts import check, safe_path, unique_object


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads((Path(__file__).resolve().parents[1]/"assets/contracts.example.json").read_text())

    def test_example_is_valid_but_explicitly_incomplete(self):
        result = check(self.spec)
        self.assertEqual(result['contract_errors'], [])
        self.assertGreater(len(result['uncovered']), 0)
        self.assertEqual(result['certification'], 'not assessed')

    def test_duplicate_id(self):
        self.spec['assets'].append(copy.deepcopy(self.spec['assets'][0]))
        self.assertTrue(any('duplicate ID' in e for e in check(self.spec)['contract_errors']))

    def test_missing_producer(self):
        self.spec['assets'][0]['producer_task'] = 'absent'
        self.assertTrue(any('unknown producer' in e for e in check(self.spec)['contract_errors']))

    def test_cycle(self):
        self.spec['tasks'][0]['dependencies'] = ['TASK-001']
        self.assertTrue(any('cycle' in e for e in check(self.spec)['contract_errors']))

    def test_input_overwrite_and_ambiguous_output(self):
        self.spec['tasks'][0]['output_paths'].append('data/prepared/panel.csv')
        other = copy.deepcopy(self.spec['tasks'][0]); other['id'] = 'TASK-002'
        self.spec['tasks'].append(other)
        errors = check(self.spec)['contract_errors']
        self.assertTrue(any('overwrites' in e for e in errors))
        self.assertTrue(any('already owned' in e for e in errors))

    def test_path_escape(self):
        for path in ['.', '../x', '/data/x', 'a/../x', './x', 'a//x', 'C:\\x', '$HOME/x', '~user/x', '.git/config', 'https://x/y']:
            self.assertFalse(safe_path(path), path)
        self.assertTrue(safe_path('data/a file.csv'))

    def test_verified_metadata_does_not_certify(self):
        self.spec['inputs'][0].update(sha256='a'*64, data_class='restricted')
        self.spec['tasks'][0]['command'] = 'python code/build_figure.py'
        self.spec['results'][0].update(status='verified', receipt='runs/example/receipt.json')
        self.spec['results'][0]['comparison']['unit'] = 'index'
        result = check(self.spec)
        self.assertEqual(result['contract_errors'], [])
        self.assertEqual(result['uncovered'], [])
        self.assertEqual(result['certification'], 'not assessed')

    def test_verified_requires_receipt(self):
        self.spec['results'][0]['status'] = 'verified'
        self.assertTrue(any('receipt' in e for e in check(self.spec)['contract_errors']))

    def test_malformed_and_missing_references(self):
        self.spec['inputs'][0]['sha256'] = 'wrong'
        self.spec['results'][0]['asset_ids'] = ['missing']
        errors = check(self.spec)['contract_errors']
        self.assertTrue(any('SHA-256' in e for e in errors))
        self.assertTrue(any('unknown asset' in e for e in errors))

    def test_duplicate_json_keys(self):
        with self.assertRaises(ValueError):
            json.loads('{"x": 1, "x": 2}', object_pairs_hook=unique_object)

    def test_malformed_field_types(self):
        self.spec['inputs'][0]['data_class'] = {}
        self.spec['assets'][0].update(kind=[], producer_task=[], provenance_status={})
        self.spec['results'][0].update(kind={}, status=[])
        self.assertGreater(len(check(self.spec)['contract_errors']), 0)

    def test_long_serial_sequence(self):
        self.spec['tasks'] = [dict(id=f'T-{n}', input_ids=[], dependencies=[f'T-{n-1}'] if n else [],
                                   code_paths=['code/solve.py'], output_paths=[f'build/{n}.csv'], command='python code/solve.py')
                              for n in range(1500)]
        self.spec['assets'][0].update(producer_task='T-1499', path='build/1499.csv')
        self.spec['results'][0]['producer_task'] = 'T-1499'
        self.assertEqual(check(self.spec)['contract_errors'], [])

    def test_manual_origin_is_not_a_fake_generator(self):
        self.spec['assets'][0].update(kind='static', producer_task=None, provenance_status='manual_source', origin='Author drawing, frozen source')
        self.spec['results'][0].update(kind='authored', producer_task=None, status='documented-static', origin='Author drawing, frozen source')
        self.assertEqual(check(self.spec)['contract_errors'], [])


if __name__ == '__main__':
    unittest.main()
