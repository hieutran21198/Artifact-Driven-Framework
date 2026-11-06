# Entities

How a domain entity is written. The examples use the `book` domain of the
[reference pass](../software-knowledges/artifacts/book/specification.md).

## Naming

| Thing | Rule | Example |
| --- | --- | --- |
| Entity | A specific name that does not clash across domains; never a bare `Item` | `book.Book` |
| Entity file | snake_case of the entity | `domain/book/book.go` |

## Rules

- Fields are unexported. Callers read them through methods named after the
  field, such as `Name()`, with no `Get` prefix.
- State changes only through behavior methods, such as `Rename`, `Lend` or
  `Return`. Each method enforces its rule and returns a domain error when the
  change is not allowed. There are no setters.
- `New<Entity>` (or `New` when the package has one entity) checks every rule
  and returns a valid entity that is not stored yet.
- `Restore<Entity>` (or `Restore`) rebuilds a stored entity without checking
  the rules again. Only repositories call it.
- The zero value is not valid. Code outside the domain never builds an entity
  with a struct literal.
- Each domain declares its errors as sentinel values, such as `ErrNotFound`
  and `ErrInvalidTransition`, so callers can match them with `errors.Is`.
- New behavior is a new method. Lifecycle changes go through one place, so the
  allowed transitions stay readable.

Return to [architecture](README.md).
