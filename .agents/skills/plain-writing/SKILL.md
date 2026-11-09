---
name: plain-writing
description: >-
  Write or review the text of a page - a site page, a README, the prose around
  knowledge - so a reader gets its value in five seconds. A picture first,
  then results and "Label: value" lines; no lead-ins, stories, selling,
  comparisons or lists that only show breadth. Use before showing or
  publishing other pages, and when asked to review or shorten their text. For
  landing-page work, use the landing-page skill instead.
---

# Plain writing

For landing-page work, use [landing-page](../landing-page/SKILL.md) instead
of the form and cuts below.

The language rules are in [Files and prose](../../../docs/coding-standards/README.md#files-and-prose)
and [ASD-STE-100](../../../docs/coding-standards/asd-ste-100/README.md). This
skill adds the form of a page and the cuts, by example.

## Form

1. **Picture first.** Under each heading, put the thing that shows the value:
   a diagram, a table, a file tree, a worked example. Text labels it.
2. **Results, not lead-ins.** Each line states a result or a fact as
   "Label: value". Role lines are "Role: verb, verb".
3. **One fact once** on a page.

## Cut

Delete the sentence. If the reader still knows what to do, it stays deleted.
Cut on sight:

- an intro or a line about the page itself;
- a story, even a concrete one;
- a benefit, a speed, "no cost", a selling heading;
- a comparison, pros and cons, a "why";
- a list of practices or tools that only shows breadth;
- a term or ID with no plain meaning next to it;
- a closing line.

## Examples

Each row is a cut a reviewer made on a real page.

| Before | After |
| --- | --- |
| A workspace tells a coding agent how the team works: who does each step, with which skill, and what each one may change. This page shows what is in the workspace… | (cut) |
| Every new workspace has these files. The copies in `.agents` are the ones to change; `.claude` only links to them. | (cut: the file tree shows it) |
| Write the rules of a product before its code, and trace each rule to its tests. | (cut: no reader knows yet what a rule is) |
| Nothing new. Artifact Driven invents no method. It puts practices… in one place. | (cut) |
| A table: a usual brainstorm beside shaping a need, with pros and cons. | (cut) |
| Why shape a need first: to brainstorm a change, people read everything… | (cut) |
| How to break down a requirement | Break down the requirement |
| One change, from the issue to the pull request | Issue to pull request |
| Who needs what, and how you will know it is done. | A member can borrow a book and sees when it is due. |
| Writes the need and the criteria, answers the questions, and approves the goal. | Product owner: gather information, write the criteria, approve the goal |
| Read each step and write down what must stay true. Words such as "must", "only" and "at most" point to a rule. | Only a book on the shelf can be lent. |
| The scan reads the test files for rule IDs… A rule it finds has a test; the code may still be wrong. The impact follows the links… | (cut: the home page needs neither) |
| The issue: lend books for 21 days by default, not 14. In the sample, one rule holds the default: BK-4 of Books, "a borrowed book is due back 14 days later". | Issue: lend books for 21 days, not 14. Rule: BK-4, due back 14 days later. |
| BK-4 reaches 6 criteria of Borrow a book, 14 scenarios of Borrowing and Returning, and the Books pages of both apps. The checks pass. | Reach: 6 criteria, 14 scenarios, the Books pages of both apps. Checks: pass. |

## Review

1. Read only the headings and the pictures. If the value is not clear in five
   seconds, the page needs a better picture, not more text.
2. Read each line against the examples above. Rewrite to the form; do not
   patch a sentence with another sentence.
3. Report each cut as before and after.
