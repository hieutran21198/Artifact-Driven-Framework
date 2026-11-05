# Diagrams

Which diagrams the documentation carries and how to draw them.

## Rules

- Draw diagrams in Mermaid, inside the Markdown page they explain.
- The text or the source code is the authority. A diagram never adds a fact
  that the text or the source does not hold.
- One diagram answers one question. Say the question, or the source, in the
  sentence above the diagram.
- Use only `flowchart`, `sequenceDiagram`, `classDiagram` and
  `stateDiagram-v2`.
- Update the diagram in the same change as the text or the source it draws.

## Catalog

| Docs | Diagram | Type | Page |
| --- | --- | --- | --- |
| Software knowledge | One set per layer, as listed in [Diagrams](../artifact-driven/knowledge.md#diagrams) | — | The layer's page |
| Governance | Who does each step and who hands off to whom | `flowchart` | [Team](../artifact-driven/team.md) |

A new page adds a diagram only when it answers a question the text answers
slowly, and adds a row here. A project adds rows for its own architecture and
infrastructure pages.

## Not drawn

- The database schema. The artifact `classDiagram` shows what each entity
  holds.
- Calls between domains. Domains are a unit of knowledge, not a boundary in
  the code, so these calls are plain function calls.

Return to [documentation](../README.md).
