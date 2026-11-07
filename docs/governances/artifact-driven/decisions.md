# Decisions

Why Artifact Driven is shaped the way it is: each decision, what it was chosen
over, and what it costs. A rule in [Knowledge](knowledge.md) or a runbook says
what to do; this page says why. Revisit a decision when its "Revisit when"
comes true, and record the new one here.

## OpenAPI holds every contract, also what is not HTTP

**Decision.** Every contract is an OpenAPI 3.0.3 file, whatever crosses it.
What OpenAPI has no place for goes under a root key that starts with `x-`:

| Crosses | Where |
| --- | --- |
| An HTTP request | `paths`, as OpenAPI defines it |
| A timer, a schedule or a message that starts a worker | `x-triggers` |
| A command that is not an HTTP request, such as a CLI command or an action in a client's interface | `x-commands` |
| A payload: a message, an email, a push, a file, a configuration | `components/schemas`, as JSON Schema |

**Context.** OpenAPI describes HTTP APIs only: each path is an HTTP method on a
URL. A product also has workers, messages, command-line tools and actions in
its user interface, and each scenario must name what starts it, so that the
checks and the impact analysis can trace it.

**Options.**

| Option | For | Against |
| --- | --- | --- |
| OpenAPI with `x-` keys (chosen) | One file format and one parser for the scripts; one place per flow or artifact for everything that crosses it; payloads stay JSON Schema | The `x-` keys are this framework's own: other OpenAPI tools ignore them, and a reader must learn them |
| A standard per kind: OpenAPI, AsyncAPI for messages, a format of our own for commands | Each kind in the format made for it; AsyncAPI tools work on the messages | Two or three formats to learn, lint and parse; a flow's contract split over several files; still no standard for commands |
| Plain text in the flow, no contract | Nothing to declare | The checks cannot tell a named command from a typo, and impact cannot trace it |

**Costs.** OpenAPI tools, such as a generated client or the documentation
viewer of a vendor, show the `x-` keys as unknown and generate nothing for
them. Redocly lint accepts them. The framework's scripts read them.

**Revisit when** a project needs the tools of another standard for one kind,
such as AsyncAPI code generation for its messages. Then that kind moves to its
standard, and the scripts learn to read it.

Return to [Artifact Driven](README.md).
