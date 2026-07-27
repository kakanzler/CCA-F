# Sampling walkthrough

1. initiating sampling
   - On the server, during a tool call, run the `create_message()` method, passing in some messages that you wish to send to a language model.
   - `server.py`: see the row; `result = ...`
    ```python
    from mcp.server.fastmcp import FastMCP, Context
    from mcp.types import SamplingMessage, TextContent

    mcp = FastMCP(name="Demo Server")


    @mcp.tool()
    async def summarize(text_to_summarize: str, ctx: Context):
        prompt = f"""
            Please summarize the following text:
            {text_to_summarize}
        """

        result = await ctx.session.create_message(
            messages=[
                SamplingMessage(
                    role="user", content=TextContent(type="text", text=prompt)
                )
            ],
            max_tokens=4000,
            system_prompt="You are a helpful research assistant.",
        )

        if result.content.type == "text":
            return result.content.text
        else:
            raise ValueError("Sampling failed")


    if __name__ == "__main__":
        mcp.run(transport="stdio")

    ```
2. Sampling callbacks
   - On the client, you must implement a sampling callback. It will receive a list of messages provided by the server.
   - `client.py` : see `def sampling_callback()`
    ```python
    import asyncio
    from anthropic import AsyncAnthropic
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    from mcp.client.session import RequestContext
    from mcp.types import (
        CreateMessageRequestParams,
        CreateMessageResult,
        TextContent,
        SamplingMessage,
    )

    anthropic_client = AsyncAnthropic()
    model = "claude-sonnet-4-0"

    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server.py"],
    )


    async def chat(input_messages: list[SamplingMessage], max_tokens=4000):
        messages = []
        for msg in input_messages:
            if msg.role == "user" and msg.content.type == "text":
                content = (
                    msg.content.text
                    if hasattr(msg.content, "text")
                    else str(msg.content)
                )
                messages.append({"role": "user", "content": content})
            elif msg.role == "assistant" and msg.content.type == "text":
                content = (
                    msg.content.text
                    if hasattr(msg.content, "text")
                    else str(msg.content)
                )
                messages.append({"role": "assistant", "content": content})

        response = await anthropic_client.messages.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
        )

        text = "".join([p.text for p in response.content if p.type == "text"])
        return text


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


    async def run():
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(
                read, write, sampling_callback=sampling_callback
            ) as session:
                await session.initialize()

                result = await session.call_tool(
                    name="summarize",
                    arguments={"text_to_summarize": "lots of text"},
                )
                print(result.content)


    if __name__ == "__main__":
        import asyncio

        asyncio.run(run())

    ```
3. Message formats
   - The list of messages provided by the server are formatted for communicatino in MCP. The individual messages aren't guaranteed to be compatible with whatever LLM SDK you are using.
   - For example, if you're using the Anthropic SDK, you;ll have to write a little bit of conversion logic to turn the MCP messages into a format compatible with Anthropic's SDK.
   - `client.py`: see in the `chat()`
    ```python
    ...

    async def chat(input_messages: list[SamplingMessage], max_tokens=4000):
        messages = []
        for msg in input_messages:
            if msg.role == "user" and msg.content.type == "text":
                content = (
                    msg.content.text
                    if hasattr(msg.content, "text")
                    else str(msg.content)
                )
                messages.append({"role": "user", "content": content})
            elif msg.role == "assistant" and msg.content.type == "text":
                content = (
                    msg.content.text
                    if hasattr(msg.content, "text")
                    else str(msg.content)
                )
                messages.append({"role": "assistant", "content": content})

        response = ...
        text = ...
        return text
    ```
4. Returning generated text
   - After generating text with the LLM, you'll return a `CreateMessageResult`, which contains the generated text.
   - `client.py` see the `sampling_call_back`
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
5. Connecting the callback
   - Don't forget: the callback on the client needs to be passed into the `ClientSession` call.
   - `client.py`: see in the `run()`
    ```python
    ...

    async def run():
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(
                read, write, sampling_callback=sampling_callback
            ) as session:
                await session.initialize()

                result = await session.call_tool(
                    name="summarize",
                    arguments={"text_to_summarize": "lots of text"},
                )
                print(result.content)
    ...
    ```

6. Getting the result
   - After the client has generated and returned some text, it will be sent to the server. You can do anything with this text:
     - Use it as part of workflow in your tool
     - Decide to make another sampling call
     - Return the generated text
   - `server.py` see in the `@mcp.tool()sumarize()`
```python
    ...

    result = await ctx.session.create_message(...)

    if result.content.type == "text":
        return result.content.text
    else:
        raise ValueError("Sampling failed")

    ...
```