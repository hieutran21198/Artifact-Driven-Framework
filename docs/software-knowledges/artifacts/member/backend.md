# Member in the backend

What the backend provides for this artifact.

## HTTP contract

The [contract](openapi.yaml) comes first; the backend implements it.

## Domain contract

| Interface | Operations |
| --- | --- |
| `MemberWriter` | `FindByID`, `Create`, `Update` |
| `MemberReader` | `FindByID` |

Return to [Member](README.md).
