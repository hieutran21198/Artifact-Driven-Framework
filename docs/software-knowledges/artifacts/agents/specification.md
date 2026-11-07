# Agents specification

The behavior of the page that shows how a team runs coding agents on a
workspace. It holds no knowledge of any service or flow, and restates no rule
of the team: the [team](../../../governances/artifact-driven/team.md) owns the
roles, the flow and the limits.

## Model

The page has four parts in this order: what a workspace gives an agent, how
each tool uses it, how the agents work as a team, and one change of the sample
from the issue to the pull request.

## Rules

| ID | Rule | Error |
| --- | --- | --- |
| AGT-1 | The page shows what a new workspace gives a coding agent: the project instructions in `AGENTS.md`, a `CLAUDE.md` that imports them, one agent for each role of the team in `.agents/agents` with its tools and model, the skills in `.agents/skills`, and the links in `.claude` to both. It names only files that a new workspace holds. | — |
| AGT-2 | For Claude Code, the page says what it reads from the workspace, that the main session is the coordinator and hands each step to the agent of its role, and gives a prompt for each step of the workflow. | — |
| AGT-3 | For Codex, the page says what it reads from the workspace, and that the agent files are written for Claude Code, so a Codex session asks for each subagent and points it at the file of its role. | — |
| AGT-4 | The page shows the flow of the team in its order, with the roles that run in parallel, and its limits: the reviewer is never the author, only the coordinator commits, pushes and opens pull requests and only when asked, and the owners merge. It says when one session with subagents is enough and when workers that must talk to each other need an agent team. | — |
| AGT-5 | The page follows one change of the sample from the issue to the pull request: a new default loan period, which changes the rule of the sample that sets the due time of a loan. Each step names its role, what it runs and what it passes on, with the result the real scripts give on the sample. A role the change does not need shows as skipped, with the reason. | — |
| AGT-6 | Each fact about Claude Code or Codex is one their own documentation states, and the page links that documentation. | — |
| AGT-7 | The page has a light theme only, also when the reader's system uses a dark theme. At a width of 360 px it needs no horizontal scrolling. It needs no build step and loads no script from another host. It links the landing page and the how-we-work page at its top and at its foot. | — |

Return to [Agents](README.md).
