# Book in the backend

What the backend provides for this artifact.

## HTTP contract

The [contract](openapi.yaml) comes first; the backend implements it.

## Domain contract

| Interface | Operations |
| --- | --- |
| `BookWriter` | `FindByID`, `Create`, `Update`, `FindOnLoanDueBefore` |
| `BookReader` | `FindByID`, `CountOnLoanBy` |

Return to [Book](README.md).
