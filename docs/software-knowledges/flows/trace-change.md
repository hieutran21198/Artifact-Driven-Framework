# Flow: Trace a change

A person, or a coding agent, sees what a change affects before making it, and
what a piece of knowledge relies on before building it.

- Crosses: [configuration](../artifacts/configuration/README.md) and
  [knowledge](../artifacts/knowledge/README.md), served by the `scripts`
  service.
- Contract: `traceImpact`, `traceDown`, `countImpact` and `listQuestions` in
  the [knowledge contract](../artifacts/knowledge/openapi.yaml).
- Trigger: a person or a coding agent is about to change, or to build, a part
  of the knowledge.
- Outcome: the person knows every unit and page a change affects, or relies
  on, and which open questions hold a goal.

## Steps

1. The person runs `traceImpact` with the name of what they will change: a
   knowledge ID, an operation, a page or a field. The `scripts` service finds
   the root and the knowledge folder (CFG-1, CFG-2), reads the citations
   (KN-7), resolves the name (KN-10) and lists what a change affects (KN-8).
2. Before building a criterion, a scenario or a page, the person runs
   `traceDown` with its name. The `scripts` service lists what it relies on
   (KN-9).
3. To compare goals, or to choose where a change is cheapest, the person runs
   `countImpact`. The `scripts` service counts the size of each goal and the
   blast radius of each requirement, rule and operation (KN-11).
4. Before a goal is built, the person runs `listQuestions`. The `scripts`
   service lists the open questions that hold each goal (KN-12).

```mermaid
sequenceDiagram
    actor Person as Person or coding agent
    participant Scripts as scripts service
    participant C as configuration
    participant K as knowledge

    Person->>Scripts: traceImpact, traceDown, countImpact or listQuestions
    Scripts->>C: Root, Setting(knowledge)
    Scripts->>K: Citations, OpenQuestions
    alt the name stands for nothing
        Scripts-->>Person: says so, exit 1
    else
        Scripts-->>Person: the units and pages, or the counts
    end
```

## Scenarios

| ID | Given | When | Then | Covers |
| --- | --- | --- | --- | --- |
| F-TRACE-1 | A rule that two scenarios cite, and a criterion that cites one of them | The person runs `traceImpact` with the rule | It lists the rule, both scenarios, the criterion and their pages, by kind | KN-7, KN-8 |
| F-TRACE-2 | An operation that a scenario names and whose summary cites a rule | The person runs `traceImpact` with the operation | It lists the scenario and the criteria above it, and not the rule | KN-7, KN-8 |
| F-TRACE-3 | A schema property that one schema holds and one page names in backticks | The person runs `traceImpact` with the property | It lists what a change to that schema and to that page affects | KN-10, KN-8 |
| F-TRACE-4 | A goal key with three criteria | The person runs `traceImpact` with the key | It lists what a change to each of the three criteria affects | KN-10 |
| F-TRACE-5 | A criterion proven by two scenarios that cite rules of two artifacts | The person runs `traceDown` with the criterion | It lists the scenarios, the rules, the operations they name, and the pages of the flow and of both artifacts | KN-7, KN-9 |
| F-TRACE-6 | A name that no unit has, that is no prefix, page or property, and that no page names in backticks | The person runs `traceImpact`, `traceDown` or `countImpact` with it | It exits with 1 and says nothing in the knowledge cites the name | KN-10, SYS-3 |
| F-TRACE-7 | A knowledge folder with two goals | The person runs `countImpact` with no name | It prints the size of each goal, then the blast radius of each requirement, rule and operation, the largest first | KN-11 |
| F-TRACE-8 | A rule | The person runs `countImpact` with the rule | It prints what the rule relies on and what a change to it affects, as counts | KN-11 |
| F-TRACE-9 | A rule that no scenario cites | The person runs `countImpact` with no name | The rule shows 0 scenarios | KN-11 |
| F-TRACE-10 | An open question that names a rule one goal relies on, and one that names nothing in the knowledge | The person runs `listQuestions` | The first is listed under that goal only, the second under the questions that name nothing | KN-12 |
| F-TRACE-11 | Any workspace | The person runs `traceImpact`, `traceDown`, `countImpact` or `listQuestions` | No file of the workspace changes | SYS-4 |

Return to [flows](README.md).
