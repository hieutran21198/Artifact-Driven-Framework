# Infrastructure

Where the software runs and how it gets there. The infrastructure code in the
backend is the authority. These pages explain and draw it; they copy no
configuration values and hold no secrets.

Write one page per question, and add each diagram to the
[diagrams catalog](../coding-standards/diagrams/README.md#catalog):

| Page | Answers | Diagram |
| --- | --- | --- |
| `containers.md` | What each container runs on | `flowchart` |
| `environments.md` | Which environments exist, where each one runs and how to reach it read-only | `flowchart` |
| `pipeline.md` | How a commit reaches an environment | `flowchart` |

Link each page here when it exists.

Return to [documentation](../README.md).
