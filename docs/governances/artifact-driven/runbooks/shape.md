# Shape a need into a goal

Use when a need is new or still vague: nobody can yet say who needs what and
how a person checks that it is done. When that is clear, go to
[goal](goal.md).

Sample: [Borrow a book](https://github.com/hieutran21198/Artifact-Driven-Framework/blob/main/template/docs/software-knowledges/goals/borrow-a-book.md).

Everything in steps 1 to 3 goes on the issue. The knowledge changes only in
step 4 ([questions](../workflow.md#questions)).

## Steps

1. **Know what holds today.** Find the goals, flows and rules the need
   touches: search the knowledge, and run `python3 scripts/impact.py <ID>` on
   each one. Write the IDs on the issue. When the area has no knowledge yet,
   write that no ID holds it.
2. **Lay out the options.** Write each way to meet the need, and for each one
   the IDs it keeps, changes or adds, with what `impact.py` lists for the IDs
   it changes. When the need asks for it, include an option that changes or
   withdraws an existing rule. When only one option fits, write it and say
   why. The person who raised the need picks one; the options dropped and the
   reasons stay on the issue.
3. **Ask about the chosen option.** Ask the person one question at a time,
   starting from one concrete situation. An answer becomes a draft criterion,
   scenario or rule. What they cannot settle becomes a checklist item on the
   issue.
4. **Hand over.** When a person can check each criterion and no open item
   holds the goal, write the goal ([goal](goal.md)), then its flows
   ([flow](flow.md)).

Return to [runbooks](README.md).
