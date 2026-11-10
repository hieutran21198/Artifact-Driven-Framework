# Add or change a contract

Use when an endpoint, a payload that is not an HTTP response, or a worker
trigger is new or changes. The contract is written and agreed before the code.

Samples: [book contract](https://github.com/hieutran21198/Artifact-Driven-Framework/blob/main/template/docs/software-knowledges/artifacts/book/openapi.yaml),
[Borrow a book contract](https://github.com/hieutran21198/Artifact-Driven-Framework/blob/main/template/docs/software-knowledges/flows/borrow-book.openapi.yaml).

## Choose the file

| The endpoint | Goes in |
| --- | --- |
| Is called in a flow step | `flows/<flow>.openapi.yaml` of that flow |
| Is called by several flows | The flow that defined it first; the others name its `operationId` |
| Is still in `artifacts/<artifact>/openapi.yaml` | Moves to its flow with this change, same `operationId` |
| Is called by an external system, such as a webhook | `flows/<flow>.openapi.yaml` of the flow it starts |
| A push, email or deep link a flow sends | `components/schemas` of that flow's contract |
| A timer or schedule that starts a worker | `x-triggers` of the flow it starts, with its input under `components/schemas` |
| A CLI command or an action in a client's interface | `x-commands` of the flow it belongs to, with its input and output under `components/schemas` |
| A message a service publishes to a queue or a topic | `components/schemas` of the flow that publishes it, and `x-triggers` of each flow it starts in another service |
| The model of a domain, or a reduced form of it | `components/schemas` of `artifacts/<artifact>/openapi.yaml` |
| A request or response that combines domains | `components/schemas` of the flow, with `$ref` to the artifact schemas |
| Shared parts: errors, authentication | `system/openapi.yaml` |

## Steps

1. Start from the flow steps that call a service, from a client or from
   another service. Add one path per call
   with an `operationId` in camelCase and a summary that cites the flow
   scenarios it serves. Report the `operationId`s; the knowledge writer names them in
   the flow steps.
2. Reuse schemas with `$ref`: errors and security from `system/openapi.yaml`,
   domain schemas from the artifact's file. Do not copy a schema. A schema
   the domain lacks, such as a summary, is added to the artifact, not made up
   in the flow.
3. Follow the system requirements that govern response shapes, such as a root
   object, the naming case and the time format, and the requirement on what
   each response and payload may carry to whom (SYS-5 in the reference pass).
4. Before changing an existing operation or a response field, run [impact](../../../../scripts/README.md#impact) on
   it (`python3 scripts/impact.py <operationId|field>`) to see the scenarios,
   the client pages and the steps of other services that depend on it.
5. For a change to an existing endpoint, keep what supported client versions
   and the calling services rely on (SYS-4, SYS-6). A change is breaking when
   it:
   - removes a key a client page or a calling service's flow step needs, changes a type or the meaning of a
     value, or adds an enum value a client decodes strictly;
   - adds a required request key, removes an accepted value, or tightens the
     validation of a key a released client sends;
   - changes who may call the operation, the state changes it allows, or the
     status codes and errors it returns, including a new status such as `429`;
   - removes the operation ([remove an operation](remove.md)).

   A new optional key is not breaking. Removing data a client must not see is
   not breaking either, when the key stays in a minimal form (null, empty or a
   default) that the client pages allow.
6. Before a breaking change, check whether a new key beside the old one serves
   the need; a new key is not breaking. Otherwise add a new version of the
   path (`/v2/...`) with an `operationId` that ends in its version
   (`getBookV2`). Both versions serve the same rules and differ only in shape.
   Mark the old operation `deprecated: true` and keep it until
   [remove an operation](remove.md) allows its removal. A breaking change has
   its own issue, a sub-issue of the one that needs it.
7. When a response shape changes, check the client pages that list needs for
   the `operationId` and the flow steps of other services that call it, and
   tell the owners of those clients and services on the issue
   ([client](client.md)).
8. Lint the changed files:

   ```sh
   npx @redocly/cli lint <knowledge folder>/<path>.yaml
   ```

   Errors block the change. Warnings for license, a localhost server and
   unused shared components are expected.

Then [check the docs](check.md).

Return to [runbooks](README.md).
