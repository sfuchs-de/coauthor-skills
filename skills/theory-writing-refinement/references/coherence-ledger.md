# Coherence Ledger

Use this ledger while reading. It is an internal working device unless the user requests it.

## 1. Section ledger

For each section record:

| Field | Question |
|---|---|
| Purpose | What paper-level question does this section answer? |
| Inputs | Which results or objects from earlier sections does it use? |
| Output | What claim, object, or evidence does it establish? |
| Handoff | Why does the following section become necessary? |
| Risk | What assumption or inferential step may be hidden? |

A section is disconnected when its input was not established or its output is not used later.

## 2. Subsection ledger

For each subsection write a one-sentence contract:

> Given [incoming object], this subsection establishes [output] so that [next use].

Then check:

- Does the opening sentence state the need rather than merely announce the topic?
- Does every paragraph advance the contract?
- Does the ending state the output rather than repeat the opening?
- Does the next subsection use the output by name?

## 3. Paragraph ledger

Assign each paragraph one role:

- motivate a question;
- define objects;
- derive a claim;
- interpret a result;
- present evidence;
- qualify scope;
- transition to the next operation.

Record its controlling claim and the relation of each sentence to that claim. A paragraph with
several roles may need to be split. Several adjacent one-role fragments may need to be merged.

## 4. Sentence-chain test

Label the relation between adjacent sentences:

- `D`: definition or clarification;
- `C`: cause or mechanism;
- `I`: implication or consequence;
- `E`: evidence or derivation;
- `Q`: qualification or scope;
- `X`: contrast or comparison;
- `T`: transition to a new question.

An unlabeled jump usually signals a missing premise, an ambiguous antecedent, or an unnecessary
sentence. Repair the relation in substance rather than adding "Moreover" or "In addition."

## 5. Orphan tests

Treat a unit as a suspected orphan when:

- a one-sentence paragraph has no deliberate emphasis or transition function;
- a displayed equation is neither motivated nor used;
- a notation definition is never referenced;
- a caveat appears far from the claim it limits;
- a paragraph could move anywhere in the section without changing the argument;
- a subsection is shorter than its heading and performs no independent task;
- the final paragraph of a section does not connect to the next section.

Resolve by deleting, merging, relocating, or supplying the missing logical link.

## 6. Transition test

A good transition names both sides of the move:

> The traffic statistic captures the direct accounting effect. To recover the response of prices
> and location choices, the next section differentiates the equilibrium system.

A weak transition announces sequence without logic:

> We next turn to the equilibrium model.

Keep the first form only when the stated relationship is true.
