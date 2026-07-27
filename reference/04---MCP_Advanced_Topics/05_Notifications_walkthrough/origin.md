# Notifications walkthrough

1. Tool function receives Context argument

   - Tool functions automatically receive 'Context' as their last argument. This object has methods for logging and reporting progress to the client.
    - `server.py` see `add()` method
        ```python
        from mcp.server.fastmcp import FastMCP, Context
        import asyncio

        mcp = FastMCP(name="Demo Server")


        @mcp.tool()
        async def add(a: int, b: int, ctx: Context) -> int:
            await ctx.info("Preparing to add...")
            await ctx.report_progress(20, 100)

            await asyncio.sleep(2)

            await ctx.info("OK, adding...")
            await ctx.report_progress(80, 100)

            return a + b


        if __name__ == "__main__":
            mcp.run(transport="stdio")

        ```
2. Create logs and progress with context
   - Throughout your tool function, call the `info()`, `warning()`, `debug()`, `error()` methods to log different types of messages for the client, Also call the `report_progress()` method to estimate the amount of remaining work for the tool call.
   - `server.py` see in the method; `add()`
        ```python
        ...
            await ctx.info("Preparing to add...")
            await ctx.report_progress(20, 100)

            await asyncio.sleep(2)

            await ctx.info("OK, adding...")
            await ctx.report_progress(80, 100)
        ...
        ```
3. Define callbacks on the client
   - The client needs to define logging and progress callbacks, which will automatically be called whenever the server emis log or progress messages. These callbacks should try to display the provided logging and progress data to the user.
   - `client.py` see the methods; `logging_callback()`, `print_progres_callback()`
        ```python
        ...
        async def logging_callback(params: LoggingMessageNotificationParams):
            print(params.data)


        async def print_progress_callback(
            progress: float, total: float | None, message: str | None
        ):
            if total is not None:
                percentage = (progress / total) * 100
                print(f"Progress: {progress}/{total} ({percentage:.1f}%)")
            else:
                print(f"Progress: {progress}")
        ...
        ```
4. Pass callbacks to appropirate functions
   - Make sure you provide the logging callback to the `ClientSession` and the progress callback to the `call_tool()` function
   - `client.py` see in the method; `run()`
        ```python
        ...
        async def run():
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(
                    read, write, logging_callback=logging_callback
                ) as session:
                    await session.initialize()

                    await session.call_tool(
                        name="add",
                        arguments={"a": 1, "b": 3},
                        progress_callback=print_progress_callback,
                    )
        ...
        ```