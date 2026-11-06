# Knowledge map

Goals use flows; flows cross artifacts. Artifacts are the nodes and flows the
edges between them.

```mermaid
flowchart LR
    goal_borrow{{Goal: Borrow a book}}
    flow_borrow([Flow: Borrow a book])
    flow_return([Flow: Return a book])
    book[Artifact: book]
    member[Artifact: member]

    goal_borrow --> flow_borrow & flow_return
    flow_borrow --- book & member
    flow_return --- book & member
```

| Goal | Flows | Artifacts |
| --- | --- | --- |
| [Borrow a book](../goals/borrow-a-book.md) | [Borrow a book](../flows/borrow-book.md), [Return a book](../flows/return-book.md) | [book](../artifacts/book/README.md), [member](../artifacts/member/README.md) |

Return to [system](README.md).
