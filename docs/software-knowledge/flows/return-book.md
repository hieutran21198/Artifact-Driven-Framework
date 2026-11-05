# Flow: Return a book

Reference flow with a worker. It shows a flow that a schedule starts.

- Serves: [Borrow a book](../goals/borrow-a-book.md).
- Crosses: [book](../artifacts/book/README.md) and
  [member](../artifacts/member/README.md).
- Contract: `returnBook` in [return-book.openapi.yaml](return-book.openapi.yaml),
  with the overdue email payload under its components.
- Trigger: a member returns a book on the web or the mobile app, or the
  scheduler runs the overdue worker.
- Outcome: the book is available again, or a late loan is overdue and the
  member is told.

## Steps

### Return

1. The member returns the book. The client asks the backend to end the loan
   (`returnBook`).
2. In one transaction, the backend loads the book from `book` under BK-8, ends
   the loan under BK-5 and BK-10, and stores the book. The member's count of
   loans in `member` drops with it (MBR-2).
3. The backend answers with the book, now available.

### Overdue

1. The scheduler runs the overdue worker.
2. The worker finds every loan past its due time and marks the book overdue,
   under BK-6. From then on the member may not borrow (MBR-4).
3. The worker sends the member the overdue email.

```mermaid
sequenceDiagram
    actor Member
    participant Client as Web or mobile app
    participant Scheduler
    participant Backend
    participant B as book
    participant Email as Email service

    Member->>Client: Return this book
    Client->>Backend: returnBook
    rect rgb(235, 242, 250)
        note over Backend,B: One transaction
        Backend->>B: FindByID(book)
        Backend->>B: Return
        alt book is not on loan
            B-->>Backend: ErrInvalidTransition (BK-5)
            Backend-->>Client: Refused, nothing changed
        else book is on loan or overdue
            Backend->>B: Update(book)
            Backend-->>Client: Available
        end
    end

    Scheduler->>Backend: Run the overdue worker
    Backend->>B: MarkOverdue, for each loan past its due time
    Backend->>Email: Overdue email
```

## Scenarios

| ID | Given | When | Then | Covers |
| --- | --- | --- | --- | --- |
| F-RETURN-1 | A book on loan | The member calls `returnBook` | The book is available | G-BORROW-4, BK-5 |
| F-RETURN-2 | An available book | The member calls `returnBook` | The return is refused | BK-5 |
| F-RETURN-3 | A book on loan past its due time | The overdue worker runs | The book is overdue and the member gets the overdue email | G-BORROW-5, BK-6 |
| F-RETURN-4 | An overdue book | The member calls `returnBook`, then `borrowBook` on another book | The first book is available and the second loan goes through | G-BORROW-4, BK-5, MBR-4 |
| F-RETURN-5 | An overdue book | The member calls `getBook` | The status is overdue and the due time is the one that passed | G-BORROW-5, BK-6 |
| F-RETURN-6 | A book on loan to another member | The member calls `returnBook` | The return is refused and the loan goes on | G-BORROW-2, BK-10 |

## Not covered yet

- A member who returns a book late pays no fine.

Return to [flows](README.md).
