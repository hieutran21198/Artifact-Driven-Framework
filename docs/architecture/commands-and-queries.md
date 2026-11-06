# Commands and queries

The application layer follows light CQRS: commands and queries take separate
paths in one database.

## Two paths

- A command changes state. It builds or loads domain entities, applies their
  rules and stores them through a domain `Writer`. It returns only what the
  caller needs, such as the new ID. While an existing endpoint moves into this
  structure, the command may return the response shape that the endpoint
  already has.
- A query only reads. It reads through a domain `Reader`, changes nothing and
  returns transfer objects from `app/dto`.
- A handler calls one command or one query.

## Transfer objects

`app/dto` holds data transfer objects:

- Every field is public.
- No methods.
- A constructor may build one from the data it carries, for example
  `dto.NewBook(b *book.Book) dto.Book`.

Return to [architecture](README.md).
