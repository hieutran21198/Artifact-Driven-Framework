# Start an artifact

Use when a domain gets its first knowledge.

Sample: [book artifact](../../software-knowledge/artifacts/book/README.md).

## Files

1. `artifacts/<artifact>/README.md` in the knowledge folder
2. `artifacts/<artifact>/specification.md`
3. `artifacts/<artifact>/backend.md`
4. `artifacts/<artifact>/openapi.yaml`, when it has endpoints

## Steps

1. Check that the domain is one business domain the team agrees on, and that
   no other artifact already owns it. A new domain is an architecture change
   first.
2. Pick a rule prefix of two to four capital letters that no other artifact
   uses, and write it in the README with one line on what the artifact owns.
3. Write `specification.md`: model, rules with IDs, lifecycle
   ([artifact rule](artifact-rule.md)).
4. Write `backend.md`: the domain contract, meaning the `Writer` and `Reader`
   interfaces and their operations. Name no packages, types or tables.
5. Add a contract when the artifact has its own endpoints
   ([contract](contract.md)), and client pages for the clients that use it
   ([client](client.md)).
6. When code already exists, start from what it does today. Mark anything not
   yet confirmed as an open question in the page instead of guessing.

Then [check the docs](check.md).

Return to [runbooks](README.md).
