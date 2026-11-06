# Book on the web

What the web client needs from the responses of this artifact, by
`operationId` from the [contract](openapi.yaml). A backend change keeps these
(SYS-4). Which step calls which operation is in the flow.

## Needs

### Every item

- `id` is a positive integer and `title` is a non-empty string (BK-1).
- `status` is one of `available`, `on_loan`, `overdue` or `withdrawn`.

### `getBook`

- `due_at` is present while `status` is `on_loan` or `overdue`, and null
  otherwise (BK-4, BK-5).

### `createBook`

- The new book comes back with `status` `available` (BK-2).

Return to [Book](README.md).
