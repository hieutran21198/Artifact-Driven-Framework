# YAGNI — You Aren't Gonna Need It

Implement the approved need with the simplest sufficient solution. Do not add
behavior, configuration, extension points, layers or dependencies for a
hypothetical future consumer.

Before adding a mechanism, identify the current requirement it serves and check
whether existing code already meets it. A wrapper or dependency must remove real
work or isolate a required responsibility, not merely rename calls while adding
another API to maintain.

Preserve required security, error handling, testability and domain boundaries.
YAGNI does not justify omitting them or merging responsibilities that differ.
Remove unused machinery introduced by the change; do not expand the change into
an unrelated rewrite.

Apply this with [KISS](../kiss/README.md), [DRY](../dry/README.md) and the adopted
[General standards](../../coding-standards/general/README.md). Explain material
tradeoffs in the existing review, not in a separate checklist or approval phase.

Return to [principles](../README.md).
