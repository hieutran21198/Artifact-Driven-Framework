# Book on the mobile app

What the mobile app needs from the responses of this artifact, by
`operationId` from the [contract](openapi.yaml). A backend change keeps these
(SYS-4). Which step calls which operation is in the flow.

## Needs

### Every item

- `status` is one of `available`, `on_loan`, `overdue` or `withdrawn`. The
  app decodes it strictly, so a new value is a breaking change.
- `due_at` is an RFC 3339 time when present (SYS-3).

### `getBook`

- `borrowed_by_me` is a boolean and is never null (BK-9).

### `borrowBook`

- The response is the book itself, with `status` `on_loan` and `due_at` set
  (BK-4).

### BK-4

- The app's help text states the loan period. It is the default of
  `loan_days`; a change to that default is a change to this text.

Return to [Book](README.md).
