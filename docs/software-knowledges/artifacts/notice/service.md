# Notice in the notification service

What the `notification` service, which serves this artifact, provides for it.

## HTTP contract

The [contract](openapi.yaml) comes first; the `notification` service
implements it.

## Domain contract

| Interface | Operations |
| --- | --- |
| `NoticeWriter` | `FindByKey`, `Create`, `Update` |
| `NoticeReader` | `FindByKey` |

Return to [Notice](README.md).
