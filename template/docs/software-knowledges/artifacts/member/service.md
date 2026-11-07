# Member in the lending service

What the `lending` service, which serves this artifact, provides for it.

## HTTP contract

The [contract](openapi.yaml) comes first; the `lending` service implements it.

## Domain contract

| Interface | Operations |
| --- | --- |
| `MemberWriter` | `FindByID`, `Create`, `Update` |
| `MemberReader` | `FindByID` |

Return to [Member](README.md).
