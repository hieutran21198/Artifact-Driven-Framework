# Agents specification

The explanation of how a team runs coding agents on a
workspace. It holds no knowledge of any service or flow, and restates no rule
of the team: the [team](../../../governances/artifact-driven/team.md) owns the
roles, the flow and the limits.

## Model

One sample change shows the work of people and agents together. Start gives
the reader a prompt to try it. Optional reference details hold the workspace
files, team limits and tool documentation.

## Rules

| ID | Rule | Error |
| --- | --- | --- |
| AGT-1 | The workspace reference shows the project instructions in `AGENTS.md`, a `CLAUDE.md` that imports them, the role definitions in `.agents/agents`, the skills in `.agents/skills`, and the links in `.claude` to both. Details about roles, tools and models agree with the files a new workspace holds. | — |
| AGT-2 | Withdrawn: moved to AGT-8 and AGT-9. | — |
| AGT-3 | Withdrawn: moved to AGT-8 and AGT-9. | — |
| AGT-4 | Withdrawn: moved to AGT-11. | — |
| AGT-5 | Withdrawn: moved to AGT-12. | — |
| AGT-6 | Each fact about Claude Code or Codex is one their own documentation states, and the page links that documentation. | — |
| AGT-7 | Withdrawn: moved to SYS-8. | — |
| AGT-8 | Withdrawn: moved to AGT-12. | — |
| AGT-9 | The tool reference says what Claude Code and Codex read from a workspace, and how each session uses the role instructions to hand off work. It distinguishes instructions supplied by the workspace from capabilities provided by the tool. | — |
| AGT-10 | Withdrawn: moved to AGT-13. | — |
| AGT-11 | The page explains the limits of the team: the reviewer does not review a change it wrote, roles hand their results to the coordinator, a knowledge gap found in code goes back to the knowledge writer, and only the coordinator commits, pushes and opens pull requests, only when asked. People retain the approvals assigned by the governance. | — |
| AGT-12 | The page follows one sample change from the issue to the pull request: change the default loan period from 14 to 21 days for new loans only; existing due dates stay unchanged. It identifies each step's role, runbook, agent work and human check. A step the change does not need is skipped with a reason. Any reported script output is reproducible on the sample, and an impact result is not presented as a runtime test result. | — |
| AGT-13 | Start gives a prompt for the reader's own agent to make the sample change in a new workspace, and a checklist linked to its governance: clarify the need before writing, change knowledge before code, run impact and the applicable checks, and report actual results and limits. The prompt preserves human approval and does not authorize a push or merge. The page promises no result the agent will give. | — |

Return to [Agents](README.md).
