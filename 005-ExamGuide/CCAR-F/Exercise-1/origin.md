# Exercise 1: Build a Multi-Tool Agent with Escalation Logic

- *Objective*: Practice designing an *agentic loop* with tool integration, structured error handling, andescalation patterns.

### Steps:
  1. **Define 3-4 MCP tools** with detailed descriptions that clearly differentiate each tool's purpose, expected inputs, and boundary conditions. Include at least two tools with similar functionality that require careful description to avoid selection confusion.

  2. **Implement an agentic loop** that checks stop_reason to determine whether to continue tool execution or present the final response. Handle both "tool_use" and "end_turn" stop reasons correctly.

  3. **Add structured error responses** to your tools: include errorCategory(transient/validation/permission), is Retryable boolean, and human-readable descriptions. Test that the agent handles each error type appropriately (retrying transient errors, explaining business errors to the user).

  4. Implement **a programmatic hook** that intercepts tool calls to enforce a business rule (e.g., blocking operations above a threshold amount), redirecting to an escalation workflow when triggered.

  5. **Test** with multi-concern messages (e.g., requests involving multiple issues) and **verify** the agent decomposes the request, handles each concern, and synthesizes a unified response.

### Domains reinforced:

  - Domain 1 (Agentic Architecture & Orchestration), Domain 2 (Tool Design & MCPIntegration), Domain 5 (Context Management & Reliability)