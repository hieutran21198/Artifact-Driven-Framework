# Requirements

Requirements that every goal and flow follows. A goal cites them by ID.

| ID | Requirement |
| --- | --- |
| SYS-1 | A JSON response is always a root object, never a bare array, for example `{ "data": [...] }`. |
| SYS-2 | JSON property names are `snake_case`. |
| SYS-3 | Time values are RFC 3339. |
| SYS-4 | A backend change keeps the response shape of an existing endpoint, because released client versions keep parsing it. |
| SYS-5 | A member-facing response never carries data about another member. Staff responses may. |

Return to [system](README.md).
