# Agents specification

The behavior of the page that shows how a team runs coding agents on a
workspace. It holds no knowledge of any service or flow, and restates no rule
of the team: the [team](../../../governances/artifact-driven/team.md) owns the
roles, the flow and the limits.

## Model

The page has five parts in this order: one change of the sample from the issue to the pull request, the limits of the team, the same change run by the reader's own agent, the files in a workspace, and a reference for each tool.

## Rules

| ID | Rule | Error |
| --- | --- | --- |
| AGT-1 | The page shows what a new workspace gives a coding agent: the project instructions in `AGENTS.md`, a `CLAUDE.md` that imports them, one agent for each role of the team in `.agents/agents` with its tools and model, the skills in `.agents/skills`, and the links in `.claude` to both. It names only files that a new workspace holds. | — |
| AGT-2 | Withdrawn: moved to AGT-8 and AGT-9. | — |
| AGT-3 | Withdrawn: moved to AGT-8 and AGT-9. | — |
| AGT-4 | Withdrawn: moved to AGT-11. | — |
| AGT-5 | Withdrawn: moved to AGT-12. | — |
| AGT-6 | Each fact about Claude Code or Codex is one their own documentation states, and the page links that documentation. | — |
| AGT-7 | Withdrawn: moved to SYS-8. | — |
| AGT-8 | Withdrawn: moved to AGT-12. | — |
| AGT-9 | Below the steps, as a reference, the page says what Claude Code and what Codex read from a workspace, and how a session of each hands a step to the agent of its role. | — |
| AGT-10 | Withdrawn: moved to AGT-13. | — |
| AGT-11 | After the change, the page lists the limits of the team: the reviewer never reviews a change it wrote, each role reports to the next, a gap found in code goes back to the knowledge writer, and only the coordinator commits, pushes and opens pull requests, and only when asked; the owners merge. | — |
| AGT-12 | The page follows one change of the sample from the issue to the pull request: a new default loan period, which changes the rule of the sample that sets the due time of a loan. Each step names its runbook and its role, what the agent does with the prompt that starts it, and what the person checks, with the result the real scripts give on the sample. A step the change does not need shows as skipped, with the reason. | — |
| AGT-13 | After the change of the sample, the page gives a prompt that asks the reader's own agent to make that change in a new workspace, and lists what the reader checks in the run that the limits do not already say: the agent reads the request and existing knowledge and asks only about material gaps, changes the knowledge before the code, and runs the impact and the checks and reports what they print. Each point links the governance that asks for it. The page states no result the agent will give. | — |

Return to [Agents](README.md).
