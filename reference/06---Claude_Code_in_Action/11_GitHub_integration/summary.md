# [Github integration](https://anthropic.skilljar.com/claude-code-in-action/303240)

## Summary

- Claudeには公式GitHub Integrationが提供されており、GitHub Actions の中で Claude を実行できる。
- 特に以下2つの**workflows**が提供されている。
  1. Issue と Pull Requestに対し、`@claude`とメンション可能
     - メンションを受けると以下を実行する
       - issueの要求を分析し、タスクや計画に落とし込む
       - コードベースへのフル権限によってタスクに対し自動で対応する
       - IssueやPRに対して直接Claudeが反応する
  2. プルリクの自動レビュー
     -プルリクがユーザーによって作成されると以下が走る
        - その変更を自動でレビュー(影響具合など)
        - レビュー結果をポストする

- Setup方法
  - `install-github-app` in Claude`
    - GitHubにClaude Codeをインストールする
    - API Keyを追加する
    - 自動で `.github/workflows`以下に2つのGitHub Actionをもつ**workflows**を追加するプルリクが生成される


### Note/Tips

- **workflows**はカスタマイズ可能で、プロジェクト固有の設定を反映させることもできる。
  - 環境変数の設定やMCP serverの仕様、DBを確認する際はなにをつかうか、など

- MCP Serverについては`.github/workflows/`に追加されたワークフローファイルに以下のように追記することで、設定可能。
  - ex
    ```json
    mcp_config: |
        {
            "mcpServers": {
                "playwright": {
                    "command": "npx",
                    "args": [
                        "@playwright/mcp@latest",
                        "--allowed-origins",
                        "localhost:3000;cdn.tailwindcss.com;esm.sh"
                    ]
                }
            }
        }
    ```
- その場合、GitHub Actionsでは権限設定にショートカットはないので各MCPサーバーの各ツールを個別に、明示的にPermissionsを許可すること。これも`.github/workflows/`に追加されたワークフローファイルに追記する
  - ex
    ```
    allowed_tools: "Bash(npm:*),Bash(sqlite3:*),mcp__playwright__browser_snapshot,mcp__playwright__browser_click,..."
    ```

## Supplement

- カスタマイズの具体的な手段は大きく3種類:
  1. Claude実行前の **Project Setup ステップ** : `run:` で `npm run setup` などを実行し環境を準備
  2. **`custom_instructions`** : サーバーは localhost:3000 で起動済み」「ログは logs.txt」「DBは sqlite3 CLIで参照可」等のプロジェクト文脈を文章で渡す
  3. **`mcp_config`** : MCPサーバー定義
- ベストプラクティス:
  - まずデフォルトのワークフローから始めて段階的にカスタマイズし、複雑なタスクの前にシンプルなタスクでワークフローを検証する。

## Reference

