# [Sampling](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296288)

## Summary

- **Sampling** : MCP Serverが直接Claudeに通信するのではなく、MCP Clientを介してClaudeへ通信すること
  - *利点*：
    - MCP Serverが直接する場合と比較し、MCP ServerがAPI Keyを持つ必要性がないこと
    - Claudeとの統合のためのコードを作成する必要性がないこと。（ClientはすでにClaudeと統合するコードを有している。）
    - 複雑性が増さないこと。（ClientはすでにClaudeと統合するコードを有している。）
    - 生成に必要なTokenコストは sampling でも発生するが、その支払いを **Server ではなく（既にClaude接続を持つ）Client が負担する**点。
  - *流れ*
    ```mermaid
    sequenceDiagram
        MCP Client ->> Claude : research a topic
        Claude -->> MCP Client : Run the 'research' tool
        MCP Client ->> MCP Server : Tool Call Request
        MCP Server ->> Wikipedia : Research...
        MCP Server ->> Wikipedia : Research...
        MCP Server ->> Wikipedia : Research...
        MCP Server ->> MCP Client : "Could u call Claude for me to sumarize these data?"
        MCP Client ->> Claude : call to claude on behalf of MCP Server
        Claude -->> MCP Client : respond
        MCP Client ->> MCP Server : "Here's the summarization"
    ```
  - *実装*
    - Server
        ```python
        @mcp.tool()
        async def summarize(text_to_summarize: str, ctx: Context):
            prompt = f"""
            Please summarize the following text:
            {text_to_summarize}
            """

            result = await ctx.session.create_message(
                messages=[
                    SamplingMessage(
                        role="user",
                        content=TextContent(
                            type="text",
                            text=prompt
                        )
                    )
                ],
                max_tokens=4000,
                system_prompt="You are a helpful research assistant",
            )

            if result.content.type == "text":
                return result.content.text
            else:
                raise ValueError("Sampling failed")
        ```
    - Client
        ```python
        async def sampling_callback(
            context: RequestContext, params: CreateMessageRequestParams
        ):
            # Call Claude using the Anthropic SDK
            text = await chat(params.messages)

            return CreateMessageResult(
                role="assistant",
                model=model,
                content=TextContent(type="text", text=text),
            )
        ```

### Note/Tips


## Supplement

- MCP Server - Claude 間を直接通信させる場合、ServerはAPI Keyを持つ必要がある。

- sampling が最も有効なのは「公開（public）な MCP Server」を作るとき。不特定多数のユーザーが Server 経由で無制限にテキスト生成すると、その AI コストを Server 側が全部被ることになる。sampling ならユーザー（Client）ごとに自分の分を支払うので、公開 Server でもコストが暴走しない。

## Reference

