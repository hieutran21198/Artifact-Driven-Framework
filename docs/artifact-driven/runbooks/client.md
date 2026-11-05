# Describe a client

Use when a client starts to need something from an artifact's responses, or
stops needing it, when an app team reports a change on an issue, and before
any contract change to an operation the client uses. A client page lists, by
`operationId`, what the client needs from the responses, so that a backend
change does not break it (SYS-4 in the reference pass). Which client calls
which operation is in the flow, not on this page.

Sample: [book on the mobile app](../../software-knowledge/artifacts/book/mobile.md).

## Files

1. `artifacts/<artifact>/<client>.md` in the knowledge folder, where
   `<client>` is a client name from the
   [configuration](../../../scripts/README.md#configuration)
2. The artifact's README

## Steps

1. Find the operations the client calls in the flows (each step names its
   actor and its `operationId`).
2. For a new feature, write the needs from the flow and the contract, before
   the client code exists. The page is then the brief for the app team.
3. For a client that already runs, read its code on the branch it releases
   from to learn what it depends on. Do not commit to client repositories.
4. Under `## Needs`, write what the client expects: first what every response
   item needs, then one subsection per `operationId` for anything extra. A
   need is a key that must be present or non-null, or a value with a special
   meaning. Cite a rule ID when a need follows a rule; do not restate it.
5. Write no screens, code locations or other evidence ([knowledge, not
   evidence](../knowledge.md#knowledge-not-evidence)). Report the evidence to
   the coordinator for the issue.
6. Write the brief or handoff for the app team on the issue, citing the page.
   The page never holds a brief, a handoff or a plan.
7. Link the page from the artifact's README.

The coordinator then [checks the docs](check.md).

Return to [runbooks](README.md).
