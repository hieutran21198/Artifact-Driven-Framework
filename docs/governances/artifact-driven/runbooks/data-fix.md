# Fix stored data

Use when stored data breaks a rule and the code does not change, such as two
columns that must agree and do not.

## Files

1. The rule the rows break, in its artifact's specification
2. The migration, in the code repository

## Steps

1. Name the rule the rows break, by ID. When the rule is only prose in the
   model, add it to the rules table first ([artifact rule](artifact-rule.md)).
   Choosing which value is right is a knowledge change the owner of the
   artifact decides.
2. On the issue, record the query that finds the rows and their count in each
   environment, with personal data masked.
3. Write the migration so it can run twice with the same result, and back up
   the rows it changes before it runs.
4. A test seeds rows that break the rule, runs the migration, and names the
   rule ID.
5. Fix the code that wrote the rows in the same pull request, or say on it why
   no code did.
6. Only the coordinator runs the migration in an environment, and only when
   the owner of the service that holds the data asks for that environment. After each run, record the count
   of rows that break the rule on the issue: it must be zero.

Then [check the docs](check.md).

Return to [runbooks](README.md).
