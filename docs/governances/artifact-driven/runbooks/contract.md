# Add or change a contract

Use when an endpoint, a payload that is not an HTTP response, or a worker
trigger is new or changes. The contract is written and agreed before the code.

Samples: [book contract](https://github.com/hieutran21198/Artifact-Driven-Framework/blob/main/template/docs/software-knowledges/artifacts/book/openapi.yaml),
[notice contract](https://github.com/hieutran21198/Artifact-Driven-Framework/blob/main/template/docs/software-knowledges/artifacts/notice/openapi.yaml).

## Choose the file

| The endpoint | Goes in |
| --- | --- |
| An endpoint | `artifacts/<artifact>/openapi.yaml` of the artifact whose code receives it |
| An endpoint whose use case crosses domains, such as a checkout | `openapi.yaml` of the artifact that owns its handler and use case |
| Is called by an external system, such as a webhook | `openapi.yaml` of the artifact that receives and translates the payload |
| A push, email or deep link sent to the outside | `components/schemas` of the artifact that sends it |
| A timer or schedule that starts a worker | `x-triggers` of the artifact whose worker handles it, with its input under `components/schemas` |
| A CLI command or an action in a client's interface | `x-commands` of the artifact it belongs to, with its input and output under `components/schemas` |
| A message from a queue or a topic | `x-commands` of the artifact that receives it, with its input under `components/schemas` |
| A call or a notice from one domain to another in the same service | No contract: a step of the flow; the signature stays in code |
| Shared parts: errors, authentication | `system/openapi.yaml` |

## Steps

1. Start from the flow steps that call a service, from a client or from
   another service. Add one path per call
   with an `operationId` in camelCase and a summary of what it does. The
   summary need not cite IDs: the scenarios that name the operation link it to
   its rules ([citations](../knowledge.md#citations)). Report the `operationId`s; the knowledge writer names them in
   the flow steps.
2. Reuse schemas with `$ref`: errors and security from `system/openapi.yaml`,
   artifact schemas from the artifact's file. Do not copy a schema.
3. Follow the system requirements that govern response shapes, such as a root
   object, the naming case and the time format, and the requirement on what
   each response and payload may carry to whom (SYS-5 in the reference pass).
4. Before changing an existing operation or a response field, run [impact](../../../../scripts/README.md#impact) on
   it (`python3 scripts/impact.py <operationId|field>`) to see the operations,
   scenarios and flows it reaches. A field name also matches other schemas
   with a key of that name; for one schema, name it in full
   (`artifacts/<artifact>/openapi.yaml#schemas/<Schema>`). The callers are
   the clients and services that the steps, trigger and diagram of those flows
   name for each operation.
5. Decide whether the change is breaking. Every visible change to an existing
   operation is breaking, as [contracts](../knowledge.md#contracts) lists:
   for example a removed key, a changed type or meaning, a new enum value, a
   new required request key or a tighter validation. Only a new optional key
   is not breaking.
6. Do not make a breaking change in place. Add a new key beside the old one
   when that serves the need; a new optional key is not breaking. Otherwise
   add a new version of the path (`/v2/...`) with an `operationId` that ends
   in its version (`getBookV2`). Both versions serve the same rules and differ only in shape.
   Mark the old operation `deprecated: true` and keep it until
   [remove an operation](remove.md) allows its removal. A breaking change has
   its own issue, a sub-issue of the one that needs it.
7. Name on the issue the owner of each caller of step 4. Each of them reviews
   the pull request that changes the contract, and checks the decoding of
   their own part in its repository ([contracts](../knowledge.md#contracts)).
8. Lint the changed files:

   ```sh
   npx @redocly/cli lint <knowledge folder>/<path>.yaml
   ```

   Errors block the change. Warnings for license, a localhost server and
   unused shared components are expected.

Then [check the docs](check.md).

Return to [runbooks](README.md).
