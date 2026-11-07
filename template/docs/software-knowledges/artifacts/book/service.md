# Book in the lending service

What the `lending` service, which serves this artifact, provides for it.

## HTTP contract

The [contract](openapi.yaml) comes first; the `lending` service implements it.

## Domain contract

| Interface | Operations |
| --- | --- |
| `BookWriter` | `FindByID`, `Create`, `Update`, `FindOnLoanDueBefore` |
| `BookReader` | `FindByID`, `CountOnLoanBy` |

Return to [Book](README.md).
