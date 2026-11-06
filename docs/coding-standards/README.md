# Repository conventions

These conventions apply to this workspace. The language standards apply to the
backend, in the structure the [architecture](../architecture/README.md) describes.

## Standards

General owns the shared rule conventions used by the Go standard.

- [General](general/README.md): cross-language rules, levels, IDs and exceptions.
- [Go](golang/README.md): Go code in the backend; requires General.
- [ASD-STE-100 principles](asd-ste-100/README.md): clear English technical
  writing that preserves meaning. It does not certify formal ASD-STE100
  compliance.
- [Diagrams](diagrams/README.md): which diagrams the documentation carries and
  how to draw them.

## Directories and navigation

- Use lowercase kebab-case for new directory names.
- Put a file named `README.md` in every directory, including intermediate
  directories. Generated, ignored directories, Git internals and the contents of
  submodules are excluded.
- Explain the directory's purpose, current contents and relevant commands in
  its README.
- Link each child directory's README from its parent README. Include a link
  back to the parent in each child README.
- Create a directory only when its purpose can be explained.

## Files and prose

- Use UTF-8 text, LF line endings and a final newline. Follow
  [`.editorconfig`](../../.editorconfig).
- Write short, factual explanations. Distinguish proposals from accepted
  decisions and available commands from planned capabilities.
- Keep one authoritative copy of a rule or explanation. Link to that copy.
- Use relative links for repository files and check that their targets exist.
- Do not commit credentials, populated environment files or generated output.

## Validation

[The structure check](../../scripts/README.md) verifies README coverage. Review
the README contents and navigation links as part of the change; the check does
not judge their quality or approve decisions.

Return to [documentation](../README.md).
