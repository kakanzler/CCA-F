# [MCP](https://anthropic.skilljar.com/claude-code-101/469797)

## Summary

- MCP(Model Context Protocol ) : ClaudeにおいてはClaudeがユーザーのPromptから解釈した必要性に応じて外部のリソース(DB, App, Public Repository etc.)との連携を利用し、必要なAction（取得・作成・更新・アクション実行）を実行する機能を指す。
- `/claude mcp add`: MCPサーバーを追加する
  - サーバーには2種ある
    - **HTTP Server**  : リモートサーバー用。ほかのサービスが提供しているもの、自分で作成したほかのネットワークにあるものと連携するときに使う。  
    - **Stdio Server** : ローカルサーバー用。自身のPC内にMCPサーバーを建て、連携する際に使う。
- `/mcp`: 現在どのMCPサーバーと連携していて、どのようなステータスかを確認し、有効/無効の切り替え管理も可能なコマンド
- Scope : 追加するMCPサーバーを適用する範囲を設定することができる 
  - **Local**   : 現在のプロジェクトのみに適用
  - **User**    : ユーザーのすべてのプロジェクトに適用
  - **Project** : プロジェクトのRootに`.mcp.json`を配置、バージョン管理することで、Project Member全員に適用

### Note/Tips

- MCPサーバーは連携すればするほど、利用しているかに依らず、そのMCPサーバーの定義がContext Windowを占有するので不要なMCPサーバーの連携は非有効化するのが望ましい
- `gh`や`aws`のようなほとんど同等のCLIコマンドが用意されている場合はそちらを利用するほうがContext効率が良いので推奨されている
- また`Skills`はClaudeが必要になったときのみContext Windowを消費するのでContext効率が良いのでSkillsで代替可能な場合はこちらも推奨される。
- MCPサーバーの連携がContext Windowの10％を超える場合、Claude Codeは自動でTool search modeに切り替え、必要性に応じたオンデマンドにツールを利用するようになるが、必要性の判断が確実ではないので、応答精度が落ちる可能性があるので注意

## Supplement（Claude Code CLIでのSkills）

- ClaudeがMCPサーバーを通じて実行する例
  - `read` : サービス内の項目を取得
  - `query` : DBへqueryを投げる
  - `write` : サービス内の項目への記載
  - `mutate` : DBへのレコード追加、列や行の追加
  - `search` : リソース内の検索
  - `fire` : ほかアクションをトリガー

## Reference
