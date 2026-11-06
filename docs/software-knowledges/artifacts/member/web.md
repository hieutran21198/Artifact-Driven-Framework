# Member on the web

What the web client needs from the responses of this artifact, by
`operationId` from the [contract](openapi.yaml). A backend change keeps these
(SYS-4). Which step calls which operation is in the flow.

## Needs

### `getMyMember`

- `loan_count` and `loan_limit` are integers and are never null (MBR-2).
- `can_borrow` is a boolean and is false whenever MBR-2, MBR-3 or MBR-4
  refuses a loan.

Return to [Member](README.md).
