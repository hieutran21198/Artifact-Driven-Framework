# Test specification

Which knowledge IDs the test files of a part name, and how strongly each one
is proved. It holds no knowledge of any service or flow.

## Model

```mermaid
classDiagram
    class TestFile {
        +NamedIDs()
    }
    class Coverage {
        +Share(ids)
    }
    class Fragility {
        +Score(unit)
    }
    Coverage --> TestFile
    Fragility --> TestFile
```

A test file is read as text and never run (SYS-6).

## Rules

| ID | Rule | Error |
| --- | --- | --- |
| TST-1 | A test file names a knowledge ID when the ID is anywhere in its text, such as in a docstring or a comment. A file names each ID once, however often it holds it. | — |
| TST-2 | A test file names only knowledge IDs that the knowledge defines and has not withdrawn. An ID whose full prefix (all parts before the final number) no defined ID has is not a knowledge ID of the workspace, and this rule does not apply to it. This includes an unknown Flow-rule scope; an undefined numeric ID under a known scope is an unknown ID. | `ErrUnknownID` |
| TST-3 | A knowledge ID is tested when at least one test file names it. Tested says nothing about whether a test passes or proves the rule. | — |
| TST-4 | The coverage of a set of knowledge IDs gives, for criteria, scenarios and rules, how many are tested out of how many, and the tested share of all of them as a whole percent. Rules aggregate artifact rules and Flow rules as classified by KN-13; a tested Flow rule does not count as a tested scenario. Withdrawn IDs are not counted. System requirements are not in a goal's share; one line of their own gives how many of them are tested out of how many, and which are not. | — |
| TST-5 | Withdrawn: moved to TST-7. | — |
| TST-6 | A check of the tests with no folder given needs the tests folder of at least one part with a tests setting. When the configuration gives parts a tests setting and none of their tests folders exists, the check cannot run; when it gives none, there is nothing to check. | — |
| TST-7 | The fragility of a requirement, a rule, an operation or a schema is its reach times one plus its weakness, plus 8 when an open question names it. Reach counts the scenarios and criteria a change to it affects, and its operations twice. Weakness adds 1 for a knowledge ID that no scenario cites, and 1 for a knowledge ID that no test file names when test files are read. | — |

Return to [Test](README.md).
