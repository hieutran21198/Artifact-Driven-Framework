# Add or change a contract

Use when an endpoint is new or changes. The contract is written and agreed
before the code.

Samples: [book contract](../../software-knowledge/artifacts/book/openapi.yaml),
[Borrow a book contract](../../software-knowledge/flows/borrow-book.openapi.yaml).

## Choose the file

| The endpoint | Goes in |
| --- | --- |
| Touches one artifact | `artifacts/<artifact>/openapi.yaml` |
| Crosses artifacts | `flows/<flow>.openapi.yaml` |
| Shared parts: errors, authentication | `system/openapi.yaml` |

## Steps

1. Start from the flow steps that call the backend. Add one path per call
   with an `operationId` in camelCase and a summary that cites the IDs it
   serves: artifact rules in an artifact contract, flow scenarios in a flow
   contract. Report the `operationId`s; the knowledge writer names them in
   the flow steps.
2. Reuse schemas with `$ref`: errors and security from `system/openapi.yaml`,
   artifact schemas from the artifact's file. Do not copy a schema.
3. Follow the system requirements that govern response shapes, such as a root
   object, the naming case and the time format.
4. Before changing an existing operation or a response field, run [impact](../../../scripts/README.md#impact) on
   it (`python3 scripts/impact.py <operationId|field>`) to see the scenarios
   and the client pages that depend on it.
5. For a change to an existing endpoint, keep the response shape that released
   clients parse. A change is breaking when it removes a key a client page
   needs, changes a type or the meaning of a value, or adds an enum value a
   client decodes strictly. A new optional key is not breaking. A breaking
   change needs a new path or version and its own issue.
6. When a response shape changes, check the client pages that list needs for
   the `operationId`, and brief the app team ([client](client.md)).
7. Lint the changed files:

   ```sh
   npx @redocly/cli lint <knowledge folder>/<path>.yaml
   ```

   Errors block the change. Warnings for license, a localhost server and
   unused shared components are expected.

Then [check the docs](check.md).

Return to [runbooks](README.md).
