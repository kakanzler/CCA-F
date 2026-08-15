# Section Overview: **Claude Code 101**

## Differences

|  |CLAUDE.md | subagents | skills | MCP | hooks |
|---|---|---|---|---|---|
| **Feature** | Claude must follow the written rules for every query | Claude can improve context window efficiency by delegating the broken-down tasks to subagents |  Claude can automatically use specific procedures as needed | Claude can use external tools | Claude must execute the operation you defined at a specific time |
| **Timing** | deterministic (every conversation) | on-demand (Claude decides) | on-demand (Claude decides) | on-demand (Claude decides) | deterministic (defined event) |
| **Example** | company guideline | reading long text like research docs | reviewing a PR | put/read DB records | logging after processing your query |

