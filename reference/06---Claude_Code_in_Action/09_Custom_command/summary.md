# [Custom commands](https://anthropic.skilljar.com/claude-code-in-action/303234)

## Summary

- Custom Command
  - 作成方法
    - 配置場所
      - 対象のリポジトリ内の`.claude/commands/COMMAND_NAME.md`
      - ファイル名（拡張子を除く）がそのままコマンド名になる（`audit.md` → `/audit`）
    - 引数を指定したい場合
      - `Custom Command.md`内で引数として渡したい箇所を`$ARGUMENTS`と記載し、 実行時 `/COMMAND brahbrahbrah`とコマンドの後に文字列を書いてやればClaudeはそれを解釈してくれる。

    - メリット
      - 繰り返し使用する特定の一連の処理を1つのコマンドでパッケージングできるため、特定の処理をさせたいときに安定性が増す
      - Claudeは余計な推論をはさまず一連の処理をシンプルに実行するため、様々な推論ののちに一連の処理をするよりも、Context Windowの効率が良いと言えるだろう
      - さらに、Placeholderを使用することで、柔軟性も担保できる

### Note/Tips


## Supplement

- コマンドファイルを作成すると Claude Code が自動的に拾うため、再起動は不要。

- `$AUGUMENT` は 英語でDollar sign augumentと発音する。
- こういった、あとから確定した情報におきけるための仮の値をPlaceholderという。


## Reference

