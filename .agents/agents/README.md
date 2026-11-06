# Agent team

The agent definitions for the roles in
[Team](../../docs/governances/artifact-driven/team.md). That page owns the roles, the flow
and the limits; this folder only configures each agent. Claude Code reads
these files through `.claude/agents`. The main session is the coordinator and
has no file here.

| Agent | Tools | Model |
| --- | --- | --- |
| [knowledge-writer](knowledge-writer.md) | Read, Grep, Glob, Edit, Write, Bash | Default |
| [contract-designer](contract-designer.md) | Read, Grep, Glob, Edit, Write, Bash | Default |
| [client-analyst](client-analyst.md) | Read, Grep, Glob, Write | `sonnet` |
| [backend-implementer](backend-implementer.md) | Read, Grep, Glob, Edit, Write, Bash | Default |
| [defect-investigator](defect-investigator.md) | Read, Grep, Glob, Bash | `opus` |
| [reviewer](reviewer.md) | Read, Grep, Glob, Bash | `opus` |

Each file has a frontmatter (`name`, `description`, `tools`, and `model` when it
differs from the default) and a short brief: the skill to use, where the agent
may write, and what it reports. Change a role in the Team page first, then the
agent file. A project fills in the defect investigator's read-only commands.

Return to [agent resources](../README.md).
