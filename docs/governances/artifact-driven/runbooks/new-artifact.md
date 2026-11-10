# Start an artifact

Use when a domain gets its first knowledge.

Sample: [book artifact](https://github.com/hieutran21198/Artifact-Driven-Framework/blob/main/template/docs/software-knowledges/artifacts/book/README.md).

## Files

1. `artifacts/<artifact>/README.md` in the knowledge folder
2. `artifacts/<artifact>/specification.md`
3. `artifacts/<artifact>/openapi.yaml`, when its code receives calls:
   endpoints, triggers or commands

An artifact has no other file ([artifact files](../knowledge.md#artifact-files)).

## Steps

1. Check that the domain is in the
   [domain map](../../../architecture/domain-map.md). A new domain is an
   architecture change first.
2. Pick a rule prefix of two to four capital letters that no other artifact
   uses, and write it in the README with one line on what the artifact owns
   and a link to the domain map for the service that serves it.
3. Write `specification.md`: model, rules with IDs, lifecycle
   ([artifact rule](artifact-rule.md)).
4. Add a contract when the artifact has its own endpoints
   ([contract](contract.md)). The flows say which client calls each
   operation.
5. When code already exists, start from what it does today. Ask about anything
   not yet confirmed instead of guessing ([questions](../workflow.md#questions)), and
   settle each conflict with the intended behavior as
   [knowledge and running code](../knowledge.md#knowledge-and-running-code)
   says.

Then [check the docs](check.md).

Return to [runbooks](README.md).
