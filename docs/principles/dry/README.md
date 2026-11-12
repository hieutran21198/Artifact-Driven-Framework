# DRY — Don't Repeat Yourself

Keep one authoritative implementation of the same knowledge or behavior.
Before adding a helper, validator, adapter or component, inspect the existing
code and its callers for an implementation to reuse or extend.

When consumers need the same behavior and constraints, reuse that implementation
at the narrowest suitable scope. Do not copy it into another package or create a
second wrapper that repeats it. Update affected callers and tests together.

Similar syntax alone does not establish shared behavior. Keep separate domain
policies or boundary responsibilities when they have different contracts or
reasons to change. Do not force them through flags, a catch-all utility package,
or a cross-domain dependency merely to reduce duplicated lines.

Apply this with [KISS](../kiss/README.md), [YAGNI](../yagni/README.md) and the
adopted [General standards](../../coding-standards/general/README.md). Review the
actual implementation and callers, not just the proposed reuse. Keep findings
on the issue or pull request; no separate DRY report is needed.

Return to [principles](../README.md).
