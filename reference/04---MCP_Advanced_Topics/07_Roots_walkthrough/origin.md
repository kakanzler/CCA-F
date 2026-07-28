# Roots walkthrough

1. Defining roots
   - Ideally, a user will dictate which files/folders can be accessed by the MCP server.
   - This program is set up to accept a list of CLI arguments, which are interpretted as paths that the user wants to allow access to.
   - That list of paths is provided to the `MCPClient` down on lines 42.
   - `main.py` see the definition `root_paths` in `main()`
        ```python
        import asyncio
        import sys
        import os
        from dotenv import load_dotenv
        from contextlib import AsyncExitStack

        from mcp_client import MCPClient
        from core.claude import Claude

        from core.cli_chat import CliChat
        from core.cli import CliApp

        load_dotenv()

        # Anthropic Config
        claude_model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-0")
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")


        assert claude_model, "Error: CLAUDE_MODEL cannot be empty. Update .env"
        assert anthropic_api_key, (
            "Error: ANTHROPIC_API_KEY cannot be empty. Update .env"
        )


        async def main():
            claude_service = Claude(model=claude_model)

            # Get root directories from command line arguments
            root_paths = sys.argv[1:]
            if not root_paths:
                print("Usage: uv run main.py <root1> [root2] ...")
                print("Example: uv run main.py /path/to/videos /another/path")
                sys.exit(1)

            clients = {}

            async with AsyncExitStack() as stack:
                # Create the MCP client with the provided root directories
                doc_client = await stack.enter_async_context(
                    MCPClient(
                        command="uv", args=["run", "mcp_server.py"], roots=root_paths
                    )
                )
                clients["doc_client"] = doc_client

                chat = CliChat(
                    doc_client=doc_client,
                    clients=clients,
                    claude_service=claude_service,
                )

                cli = CliApp(chat)
                await cli.initialize()
                await cli.run()


        if __name__ == "__main__":
            if sys.platform == "win32":
                asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
            asyncio.run(main())

        ```
2. Creating root objects
   - According to the MCP spec, all roots should have a URI that begins with `file://`.
   - This function takes the list of paths of that the user provided and turns them into `Root` objects.
    - `mcp_client.py`: see the helper method : `_create_roots()`
        ```python
        from typing import Optional, Any
        from contextlib import AsyncExitStack
        from mcp import ClientSession, StdioServerParameters, types
        from mcp.client.stdio import stdio_client
        from mcp.types import Root, ListRootsResult, ErrorData
        from mcp.shared.context import RequestContext
        from pathlib import Path
        from pydantic import FileUrl

        import json
        from pydantic import AnyUrl


        class MCPClient:
            def __init__(
                self,
                command: str,
                args: list[str],
                env: Optional[dict] = None,
                roots: Optional[list[str]] = None,
            ):
                self._command = command
                self._args = args
                self._env = env
                self._roots = self._create_roots(roots) if roots else []
                self._session: Optional[ClientSession] = None
                self._exit_stack: AsyncExitStack = AsyncExitStack()

            def _create_roots(self, root_paths: list[str]) -> list[Root]:
                """Convert path strings to Root objects."""
                roots = []
                for path in root_paths:
                    p = Path(path).resolve()
                    file_url = FileUrl(f"file://{p}")
                    roots.append(Root(uri=file_url, name=p.name or "Root"))
                return roots

            async def _handle_list_roots(
                self, context: RequestContext["ClientSession", None]
            ) -> ListRootsResult | ErrorData:
                """Callback for when server requests roots."""
                return ListRootsResult(roots=self._roots)

            async def connect(self):
                server_params = StdioServerParameters(
                    command=self._command,
                    args=self._args,
                    env=self._env,
                )
                stdio_transport = await self._exit_stack.enter_async_context(
                    stdio_client(server_params)
                )
                _stdio, _write = stdio_transport
                self._session = await self._exit_stack.enter_async_context(
                    ClientSession(
                        _stdio,
                        _write,
                        list_roots_callback=self._handle_list_roots
                        if self._roots
                        else None,
                    )
                )
                await self._session.initialize()

            def session(self) -> ClientSession:
                if self._session is None:
                    raise ConnectionError(
                        "Client session not initialized or cache not populated. Call connect_to_server first."
                    )
                return self._session

            async def list_tools(self) -> list[types.Tool]:
                result = await self.session().list_tools()
                return result.tools

            async def call_tool(
                self, tool_name: str, tool_input
            ) -> types.CallToolResult | None:
                return await self.session().call_tool(tool_name, tool_input)

            async def list_prompts(self) -> list[types.Prompt]:
                result = await self.session().list_prompts()
                return result.prompts

            async def get_prompt(self, prompt_name, args: dict[str, str]):
                result = await self.session().get_prompt(prompt_name, args)
                return result.messages

            async def read_resource(self, uri: str) -> Any:
                result = await self.session().read_resource(AnyUrl(uri))
                resource = result.contents[0]

                if isinstance(resource, types.TextResourceContents):
                    if resource.mimeType == "application/json":
                        return json.loads(resource.text)

                    return resource.text

            async def cleanup(self):
                await self._exit_stack.aclose()
                self._session = None

            async def __aenter__(self):
                await self.connect()
                return self

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                await self.cleanup()

        ```
3. Roots callback
   - The client doesn't immediately provide the list of roots to the server. Instead, the server can make a request to the client at some future point in time. We make a callback that will be executed when the server requests the roots. The callback needs to return the list of roots inside of a `ListRootsResult` object.
   - This callback is passed into the ClientSession down on line 58.
   - `mcp_client.py` see the helper method `_handle_list_roots()`
        ```python
            ...
            async def _handle_list_roots(
                self, context: RequestContext["ClientSession", None]
            ) -> ListRootsResult | ErrorData:
                """Callback for when server requests roots."""
                return ListRootsResult(roots=self._roots)
            ...

            async def connect(self):
                server_params = StdioServerParameters(
                    command=self._command,
                    args=self._args,
                    env=self._env,
                )
                stdio_transport = await self._exit_stack.enter_async_context(
                    stdio_client(server_params)
                )
                _stdio, _write = stdio_transport
                self._session = await self._exit_stack.enter_async_context(
                    ClientSession(
                        _stdio,
                        _write,
                        list_roots_callback=self._handle_list_roots
                        if self._roots
                        else None,
                    )
                )
                await self._session.initialize()

        ```
4. Using the roots
   - On to the server. The server will use the roots in two scenarios:
     1. Whenever a tool attempts to access a file or folder.
     2. When a LLM(like Claude) needs to resolve a file or folder to a full path. Think of when a user says 'read the todos.txt file'- Claude needs to figure out where the text file is, and might do so by looking at the list of roots.
    - `mcp_server.py` see the method `list_roots()`
        ```python
        from pathlib import Path
        from mcp.server.fastmcp import FastMCP
        from pydantic import Field
        from mcp.server.fastmcp import Context
        from core.video_converter import VideoConverter
        from core.utils import file_url_to_path

        mcp = FastMCP("VidsMCP", log_level="ERROR")


        async def is_path_allowed(requested_path: Path, ctx: Context) -> bool:
            roots_result = await ctx.session.list_roots()
            client_roots = roots_result.roots

            if not requested_path.exists():
                return False

            if requested_path.is_file():
                requested_path = requested_path.parent

            for root in client_roots:
                root_path = file_url_to_path(root.uri)
                try:
                    requested_path.relative_to(root_path)
                    return True
                except ValueError:
                    continue

            return False


        @mcp.tool()
        async def convert_video(
            input_path: str = Field(description="Path to the input MP4 file"),
            format: str = Field(description="Output format (e.g. 'mov')"),
            *,
            ctx: Context,
        ):
            """Convert an MP4 video file to another format using ffmpeg"""
            input_file = VideoConverter.validate_input(input_path)

            # Ensure the input file is contained in a root
            if not await is_path_allowed(input_file, ctx):
                raise ValueError(f"Access to path is not allowed: {input_path}")

            return await VideoConverter.convert(input_path, format)


        @mcp.tool()
        async def list_roots(ctx: Context):
            """
            List all directories that are accessible to this server.
            These are the root directories where files can be read from or written to.
            """
            roots_result = await ctx.session.list_roots()
            client_roots = roots_result.roots

            return [file_url_to_path(root.uri) for root in client_roots]


        @mcp.tool()
        async def read_dir(
            path: str = Field(description="Path to a directory to read"),
            *,
            ctx: Context,
        ):
            """Read directory contents. Path must be within one of the client's roots."""
            requested_path = Path(path).resolve()

            if not await is_path_allowed(requested_path, ctx):
                raise ValueError("Error: can only read directories within a root")

            return [entry.name for entry in requested_path.iterdir()]


        if __name__ == "__main__":
            mcp.run(transport="stdio")

        ```
5. Accessing the roots
   - Roots are accessed by calling `ctx.session.list_roots()`
   - This sends a message back to the client, which causes it to run the root-listing callback
   - `mcp_server.py` see the `await ctx.session.list_roots()`
        ```python
        roots_result = await ctx.session.list_roots()
        ```
6. Authorizing access
   - Remember: the MCP SDK does not attempt to limit what files or folders your tools attempt to read! You must implement that check yourself.
   - Consider implementing a function like `is_path_allowed`, which will decide whether a path is accessible by comparing it to the list of roots.
   - `mcp_server.py` see the method `is_path_allowed()`
        ```python
        async def is_path_allowed(requested_path: Path, ctx: Context) -> bool:
            roots_result = await ctx.session.list_roots()
            client_roots = roots_result.roots

            if not requested_path.exists():
                return False

            if requested_path.is_file():
                requested_path = requested_path.parent

            for root in client_roots:
                root_path = file_url_to_path(root.uri)
                try:
                    requested_path.relative_to(root_path)
                    return True
                except ValueError:
                    continue

            return False
        ```
7. Authorizing access
   - Once you've put an authorization function together - like `is_path_allowed` - use it throughout your tools to ensure the requested path is accessible.
   - `mcp_server.py`: see the portion using`is_path_allowed()` in `convert_video()`
        ```python
        @mcp.tool()
        async def convert_video(
            input_path: str = Field(description="Path to the input MP4 file"),
            format: str = Field(description="Output format (e.g. 'mov')"),
            *,
            ctx: Context,
        ):
            """Convert an MP4 video file to another format using ffmpeg"""
            input_file = VideoConverter.validate_input(input_path)

            # Ensure the input file is contained in a root
            if not await is_path_allowed(input_file, ctx):
                raise ValueError(f"Access to path is not allowed: {input_path}")

            return await VideoConverter.convert(input_path, format)
        ```