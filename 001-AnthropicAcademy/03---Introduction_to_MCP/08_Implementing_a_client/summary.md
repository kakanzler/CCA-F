# [Implementing a client](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296696)

## Summary

- MCP Client: AI WorkFlowと外部ツールを統合する橋渡し(Bridge)のような存在。
  - MCP Clinet: Client Session は接続の後始末（リソース管理・クリーンアップ）が必要で、それを自動で行わせるためにラップしたカスタムクラス。
  - Client Session: 実際にMCP Serverとやり取りするインターフェース部分の設計を担う箇所

- シーケンス図での大きな二つの役割
  - ツールのリストを取得し、Claudeに渡すこと
    - `mcp.ClientSession.list_tools()`を使う
  - Claudeの要求に応じ、ToolをCallすること
    - `mcp.ClientSession.call_tool(tool_name : str, tool_input : dict)`を使う

- 単体テストは以下のコマンドで実行可能。内部でmcp_serverと接続し、利用可能なツール一覧やツール定義(必要なInputを含む)、を出力する
  ```sh
  uv run mcp_client.py
  ```

- ClaudeへのAPIリクエストを含めた全体のフローを確かる際は以下のコマンドを実行する。
  ```sh
  uv run main.py
  ```

### Note/Tips


## Supplement

- Projectでは通常、MCP Client, MCP Serverのどちらかのみを実装するというのが通常の流れ。ここでは学習のため、両方に触れている。

## Reference

