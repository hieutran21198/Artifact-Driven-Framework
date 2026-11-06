# Requirements

Requirements that every goal and flow follows. A goal cites them by ID.

| ID | Requirement |
| --- | --- |
| SYS-1 | A JSON response is always a root object, never a bare array, for example `{ "data": [...] }`. |
| SYS-2 | JSON property names are `snake_case`. |
| SYS-3 | Time values are RFC 3339. A duration is exact elapsed time unless its rule names a time zone. |
| SYS-4 | A change to a service keeps the response shape of an existing endpoint, and the shape of a message it publishes, because released client versions and other services keep parsing them. |
| SYS-5 | A member-facing response, and any push or email sent to a member, never carries data about another member. Staff responses may. |
| SYS-6 | A change to a service keeps the behavior a released client version, and every other service, relies on: the operations it calls, the requests it sends, who may call an operation, the state changes an operation allows, and the status codes and errors it returns. |
| SYS-7 | A rule that differs by region gives one value for each region the library serves, or says it does not apply there, and states which region it uses: the member's home region unless the rule names another. |
| SYS-8 | A worker trigger, and a call from another service, can arrive more than once. Handling the same trigger or call twice has the same result as handling it once. |

## Released client versions

SYS-4 and SYS-6 protect every released client version that is still
supported. A version is supported until the services force it to update. The
oldest supported version of each client is a system fact, kept in
[context](context.md#supported-client-versions), and changes only by the
decision of the client's owner on an issue.

Return to [system](README.md).
