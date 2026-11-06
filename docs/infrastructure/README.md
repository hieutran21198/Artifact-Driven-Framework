# Infrastructure

Where the software runs and how it gets there. The infrastructure code in each
service and client repository is the authority. These pages explain and draw it; they copy no
configuration values and hold no secrets.

Write one page per question, and add each diagram to the
[diagrams catalog](../coding-standards/diagrams/README.md#catalog):

| Page | Answers | Diagram |
| --- | --- | --- |
| `services.md` | What each service and client runs on, and what routes calls between them, such as an API gateway | `flowchart` |
| `environments.md` | Which environments exist, where each one runs and how to reach it read-only | `flowchart` |
| `pipeline.md` | How a commit of each part reaches an environment | `flowchart` |

Link each page here when it exists.

Return to [documentation](../README.md).
