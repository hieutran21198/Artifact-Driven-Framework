# Agents specification

The behavior of the page that shows how a team runs coding agents on a
workspace. It holds no knowledge of any service or flow, and restates no rule
of the team: the [team](../../../governances/artifact-driven/team.md) owns the
roles, the flow and the limits.

## Model

The page has six parts in this order: what a workspace gives an agent, the
work step by step, how the agents work as a team, one change of the sample
from the issue to the pull request, the same change run by the reader's own
agent, and a reference for each tool.

## Rules

| ID | Rule | Error |
| --- | --- | --- |
| AGT-1 | The page shows what a new workspace gives a coding agent: the project instructions in `AGENTS.md`, a `CLAUDE.md` that imports them, one agent for each role of the team in `.agents/agents` with its tools and model, the skills in `.agents/skills`, and the links in `.claude` to both. It names only files that a new workspace holds. | — |
| AGT-2 | Withdrawn: moved to AGT-8 and AGT-9. | — |
| AGT-3 | Withdrawn: moved to AGT-8 and AGT-9. | — |
| AGT-4 | The page shows the flow of the team in its order, with the roles that run in parallel, and its limits: the reviewer is never the author, only the coordinator commits, pushes and opens pull requests and only when asked, and the owners merge. It says when one session with subagents is enough and when workers that must talk to each other need an agent team. | — |
| AGT-5 | The page follows one change of the sample from the issue to the pull request: a new default loan period, which changes the rule of the sample that sets the due time of a loan. Each step names its role, what it runs and what it passes on, with the result the real scripts give on the sample. A role the change does not need shows as skipped, with the reason. | — |
| AGT-6 | Each fact about Claude Code or Codex is one their own documentation states, and the page links that documentation. | — |
| AGT-7 | Withdrawn: moved to SYS-8. | — |
| AGT-8 | For each step of the work, from shaping a need to the pull request, the page names its runbook and says what the person decides, what the agent does, with a prompt for it, and what the person checks. Where a step pulls rules out of a flow, the agent proposes them and the person decides (MTH-1). | — |
| AGT-9 | Below the steps, as a reference, the page says what Claude Code and what Codex read from a workspace, and how a session of each hands a step to the agent of its role. | — |
| AGT-10 | After the change of the sample, the page gives a prompt that asks the reader's own agent to make that change in a new workspace, and lists what the reader watches for: the agent asks before it writes, runs the impact of the rule, changes the knowledge before the code, runs the checks and reports their results, and does not commit or push. Each point links the governance that asks for it. The page states no result the agent will give. | — |

Return to [Agents](README.md).
