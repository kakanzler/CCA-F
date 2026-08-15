# [Define Hooks](https://anthropic.skilljar.com/claude-code-in-action/312000)

## Summary

- Hooksは、ツール呼び出しの実行**前後**に割り込んで制御する仕組み。Claudeが開発環境で何をできる／できないかを細かくコントロールできる。

- hooksを作成するステップ

  1. PreToolUse / PostToolUse のどちらを利用するか決定する。
  2. どのツールをHookさせるかを決定し、 `settings.json` に記載する。
     - Toolの種類
       - **Read** : ファイルの読み込み
       - **Edit** : 既存の単一ファイルへ書き込み
       - **MultiEdit** : 既存の複数ファイルへ書き込み
       - **Write** : ファイルが未作成の場合は作成し、ファイルに書き込む
       - **Bash** : コマンドの実行
       - **Glob** : パターンを使って、ファイルやフォルダを特定する
       - **Grep** : コンテンツの検索
       - **Task** : SubAgentを起動し、特定のタスクについて処理させる
       - **WebFetch** : 特定のページの最新情報を取得する
       - **WebSearch** : 特定のページの情報を検索する
  3. Claude(言語モデル)から、ClaudeCodeにツールの呼び出し指示がJSON形式で入力されるので、それに対するツールの呼び出しコマンドを`.claude/hooks/`以下に `{COMMAND_NAME}.sh`などを記載し、 `settings.json` にそのコマンドの呼び出しを書く。。
  4. ツールを呼び出した結果、エラーハンドリングが必要な場合は`{COMMAND_NAME}.sh` に明記する。
     - `Exit Code: 0` : 正常
     - `Exit Code: 2` : 異常 (PreToolUseの場合はブロック。) ⇒ stderrをClaudeに返却し、なぜ制限されていたのか、などをClaudeに説明する。

### Note/Tips

- MCP_Serverを追加すると利用可能なToolが変更される可能性があるので、Claudeに現在使えるToolを一覧形式でくれ、などと依頼することは度々有効。

- Hookのcommandについて、Typeがcommandの場合はシェルコマンドが実行されるので `node ~~ $PWD/hooks/read_hook.js`のようにJSのHookを起動させることも可能。シェルスクリプトのみが有効ではない点に注意。

## Supplement

- ClaudeからClaude Codeに送信されるTool呼び出しのデータ構造は以下のようなJSON形式。
    ```json
    {
        "session_id": "2d6a1e4d-6...",
        "transcript_path": "/Users/sg/...",
        "hook_event_name": "PreToolUse",
        "tool_name": "Read",
        "tool_input": {
            "file_path": "/code/queries/.env"
        }
    }
    ```

- Exit Code が0でも2でもない場合はエラーとして扱われる。<sup>[1](#ref1)</sup>

- フックのフックハンドラーのタイプは5つある<sup>[2](#ref1)</sup>
  - **commnad** : シェルコマンドを実行する
  - **http** : イベントのJSON入力をリクエストボディに入れてHTTP POSTリクエストとしてURLに送信し、結果をJSONで受信する
  - **mcp_tool** : 既に接続されているMCPサーバー上のツールを呼び出す。
  - **prompt** : Claudeの言語モデルに対し、promptを送信し、1ターンのみの通信を行いレスポンスをyes/noで受け取る
  - **agent** : Read, Grep, Globなどのツールを使用して条件を検証して決定するサブエージェントを生成する。(実験的)

## Reference
<a src="ref1"><a>
１．[Hook 出力](https://code.claude.com/docs/ja/hooks-guide#hook-output)
<a src="ref2"><a>
２．[フックハンドラーフィールド](https://code.claude.com/docs/ja/hooks#hook-handler-fields)