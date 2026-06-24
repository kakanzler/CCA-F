# [Hooks](https://anthropic.skilljar.com/claude-code-101/469798)

## Summary

- Hook: Claudeの処理において、ある特定のタイミングで必ずコマンドを実行させる機能

- 設定方法 :
  - `/hooks` : ClaudeとInteractiveに作成する場合。
  - `settings.json` in `.claude/`: 直接編集する場合

- 配置方法 : 
  - `~/.claude/settings.json` : ユーザー個人（全プロジェクト共通）
  - `.claude/settings.json` : ProjectのVersion管理対象としてここに配置することでチームメンバー全員に適用可能。
  - `.claude/settings.local.json` : Project単位のユーザー個人設定(,gitignoreでバージョン管理対象外とする)のが一般的

### Note/Tips

- Hooksを実行するタイミングは以下の通り
  - *PreToolUse*: Toolが呼ばれる前 
    - ex: Guardrail を実装する(`rm -rf`の実行、mainブランチへのコミットなど)、など
      - PreToolUse Hookはtool名と入力をstdinでJSONとして受け取り、Hook自身のExit Codeで挙動が決まる。0で続行、2でブロック（stderrがClaudeに渡る）、それ以外は停止しないエラー表示。
  - *PostToolUse*: Toolが呼ばれ実行された後
    - matcherに`"Edit|MultiEdit|Write"`を指定すると、ファイル編集Tool実行後にPrettier等で自動整形できる。`|`でOR表現。
  - *UserPromptSubmit*: Promptを投げた直後(ClaudeがPromptを処理する前に)
  - *Stop*: ClaudeがPromptを処理し終わった後
  - *Notification*: Claudeが通知を発行する際

## Supplement

- `settings.json`に関する補足
    - `CLAUDE_PROJECT_DIR` : Claude Codeがhook実行時に自動でセットする環境変数で、値はProjectルートの絶対Path。自分で定義(export)するのではなく、`command` 内で `$CLAUDE_PROJECT_DIR/.claude/hooks/xxx.sh` のように参照することで、cwdに依存せずProject内スクリプトを確実に指せる。

## Reference
