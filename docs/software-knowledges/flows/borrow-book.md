# Flow: Borrow a book

Reference flow. It shows how a flow is written.

- Crosses: [book](../artifacts/book/README.md) and
  [member](../artifacts/member/README.md).
- Contract: `borrowBook` in [borrow-book.openapi.yaml](borrow-book.openapi.yaml),
  and `getBook` in the [book contract](../artifacts/book/openapi.yaml).
- Trigger: a member asks to borrow a book on the web or the mobile app.
- Outcome: the book is on loan to the member, or nothing changes.

## Steps

1. The client asks for the book (`getBook`) and shows whether it is available.
2. The member confirms. The client asks the backend to lend the book to the
   signed-in member (`borrowBook`).
3. In one transaction, the backend:
   1. loads the member from `member` and checks that they may borrow, under
      MBR-2, MBR-3 and MBR-4;
   2. loads the book from `book`, under BK-8;
   3. lends the book to the member, under BK-3 and BK-4;
   4. stores the book.
4. The backend answers with the book, which now carries its due time.

```mermaid
sequenceDiagram
    actor Member
    participant Client as Web or mobile app
    participant Backend
    participant M as member
    participant B as book

    Member->>Client: Borrow this book
    Client->>Backend: borrowBook
    rect rgb(235, 242, 250)
        note over Backend,B: One transaction
        Backend->>M: FindByID(member)
        Backend->>M: CanBorrow
        alt member may not borrow
            M-->>Backend: ErrLoanLimit, ErrSuspended or ErrHasOverdue
            Backend-->>Client: Refused, nothing changed
        else member may borrow
            Backend->>B: FindByID(book)
            Backend->>B: Lend(member)
            alt book is not available
                B-->>Backend: ErrInvalidTransition (BK-3)
                Backend-->>Client: Refused, nothing changed
            else book is available
                Backend->>B: Update(book)
                Backend-->>Client: On loan, with due time
            end
        end
    end
```

## Scenarios

| ID | Given | When | Then | Covers |
| --- | --- | --- | --- | --- |
| F-BORROW-1 | An available book and an active member under the loan limit | The member calls `borrowBook` | The book is on loan to the member and the response carries its due time | BK-3, BK-4, SYS-3 |
| F-BORROW-2 | A book on loan to another member | The member calls `borrowBook` | The loan is refused and the book stays with the other member | BK-3 |
| F-BORROW-3 | A member who holds as many books as the loan limit | The member calls `borrowBook` | The loan is refused and the book stays available | MBR-2 |
| F-BORROW-4 | A suspended member | The member calls `borrowBook` | The loan is refused | MBR-3 |
| F-BORROW-5 | A member with an overdue loan | The member calls `borrowBook` | The loan is refused | MBR-4 |
| F-BORROW-6 | A withdrawn book | The member calls `borrowBook` | The loan is refused | BK-7 |
| F-BORROW-7 | A book on loan to another member | The member calls `getBook` | The response shows the book on loan and names no borrower | SYS-5, BK-9 |
| F-BORROW-8 | A member with an overdue loan | The member calls `getMyMember` | `can_borrow` is false, so the client can say why before the member tries | MBR-4 |
| F-BORROW-9 | No book yet | Staff call `createBook` with a title | The book is available, and a member can borrow it | BK-1, BK-2 |
| F-BORROW-10 | A book on loan | Staff call `withdrawBook` | The withdrawal is refused and the loan goes on | BK-7 |

## Open questions

- Whether a member may reserve a book that is on loan, and who gets it when
  it comes back (F-BORROW-2).

Return to [flows](README.md).
