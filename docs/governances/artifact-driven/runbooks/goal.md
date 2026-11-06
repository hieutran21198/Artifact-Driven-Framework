# Add or change a goal

Use when a business need is new, or its success criteria change.

Sample: [Borrow a book](../../../software-knowledges/goals/borrow-a-book.md).

## Files

1. `goals/<goal>.md` in the knowledge folder

## Steps

1. Name the outcome, not the screen: "Borrow a book", not "Borrow button".
2. Write the need: who wants it and why. Cite the actor from
   [context](../../../software-knowledges/system/context.md) and any system
   requirement by its `SYS` ID.
3. Write the success criteria as a table with IDs `G-<GOAL>-<n>`. Each one is
   something a person can check is true. Its Proven by column names the flow
   scenarios that prove it; it stays empty until the flow is written. When
   changing a goal, add new IDs and keep old ones; mark a dropped criterion as withdrawn instead of deleting it
   ([the life of an ID](../knowledge.md#the-life-of-an-id)). The goal key
   follows the same page.
4. List the flows that reach the goal and draw them as a `flowchart`. A flow
   that does not exist yet is the next runbook: [flow](flow.md).

Then [check the docs](check.md).

Return to [runbooks](README.md).
