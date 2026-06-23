# Overall in this section; **Claude Code 101**

## differences

|  |CLAUDE.md | subagents | skills | MCP | hooks |
|---|---|---|---|---|---|
| **Feature** | Claude must follow the written rules for every query | Claude can improve context window efficiency delegating the broken down tasks to subagents |  Claude can automatically use specific procedures as needed | Claude can use external tools | Claude must execute operation you defined in specific timing |
| **Timing** | deterministic (every conversation) | on-demand (Claude decides) | on-demand (Claude decides) | on-demand (Claude decides) | deterministic (defined event) |
| **Example** | company guideline | read long text like research docs | reviewing PR | put/read DB records | logging after processing to your query |

