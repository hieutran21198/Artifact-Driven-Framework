# Add or change a goal

Use when a business need is new, or its success criteria change. When the
need is still vague, [shape it](shape.md) first.

Sample: [Borrow a book](https://github.com/hieutran21198/Artifact-Driven-Framework/blob/main/template/docs/software-knowledges/goals/borrow-a-book.md).

## Files

1. `goals/<goal>.md` in the knowledge folder

## Steps

1. When changing a goal, run `python3 scripts/impact.py <ID>` on each
   criterion you change, and post what it lists on the issue.
2. Name the outcome, not the screen: "Borrow a book", not "Borrow button".
3. Write the need: who wants it and why. Cite the actor from
   [context](../../../software-knowledges/system/context.md) and any system
   requirement by its `SYS` ID.
4. Write the success criteria as a table with IDs `G-<GOAL>-<n>`. Each one is
   something a person can check is true. A criterion that is not clear is a
   question, not a guess ([questions](../workflow.md#questions)). Its Proven by column names the flow
   scenarios that prove it; it stays empty until the flow is written. When
   changing a goal, add new IDs and keep old ones; mark a dropped criterion as withdrawn instead of deleting it
   ([the life of an ID](../knowledge.md#the-life-of-an-id)). The goal key
   follows the same page.
5. List the flows that reach the goal and draw them as a `flowchart`. A flow
   that does not exist yet is the next runbook: [flow](flow.md).

Then [check the docs](check.md).

Return to [runbooks](README.md).
