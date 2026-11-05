# Member specification

The behavior of a member. It holds no knowledge of any container or flow.

## Model

```mermaid
classDiagram
    class Member {
        +Rename(name)
        +CanBorrow(loans, overdue)
        +Suspend()
        +Reinstate()
    }
    class Status {
        <<enumeration>>
        active
        suspended
    }
    Member --> Status
```

A member has a name and a status. They change only through the behaviors
above. A member's loans are the books on loan to them.

## Rules

| ID | Rule | Error |
| --- | --- | --- |
| MBR-1 | The name is not empty after trimming spaces. | `ErrInvalidName` |
| MBR-2 | A member holds at most three books on loan or overdue at once. | `ErrLoanLimit` |
| MBR-3 | A suspended member cannot borrow. | `ErrSuspended` |
| MBR-4 | A member with an overdue book cannot borrow until they return it. | `ErrHasOverdue` |
| MBR-5 | Looking up a member that does not exist fails. | `ErrNotFound` |

## Lifecycle

```mermaid
stateDiagram-v2
    [*] --> active: Join
    active --> suspended: Suspend
    suspended --> active: Reinstate
```

Return to [Member](README.md).
