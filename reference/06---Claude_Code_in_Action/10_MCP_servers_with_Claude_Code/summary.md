# [MCP servers with Claude Code](https://anthropic.skilljar.com/claude-code-in-action/303239)

## Summary

- MCPをClaudeに追加することでClaudeが使えるツール／能力を拡張できる
- 追加方法
  - ターミナルで以下を実行する
    ```sh
    $ claude mcp add {MCP_SEVER_NAME} {COMMAND to start MCP_server locally}
    ```
- プロジェクトにおけるMCP serverの自動使用許可
  - `.claude/settings.local.json`に以下のように`mcp__`をプレフィックスさせたMCP Serverの名前を追記する。
    ```json
    {
        "permissions" : {
            "allow" : ["mcp__{MCP_SEVER_NAME}"],
            "deny" : []
        }
    }
    ```

### Note/Tips


## Supplement

- MCP Serverはローカルだけでなくリモートでもホストでき、Claudeに「本来は持たない新しいツール・能力」を与えるものである（単なる処理速度向上ではない）。
- 原文(Origin.md)ではPlaywrith（ブラウザ操作用のMCP Server）を例に挙げている。
- MCP Serverとの連携例
  - DataBaseとの通信
  - APIのテスト、監視
  - ファイルシステムの操作
  - 他のクラウドサービスとの連携
  - 開発ツールの自動化
  - etc.

## Reference

