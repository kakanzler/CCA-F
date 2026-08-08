# [Agents and tools](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287803)

## Summary

- **Agents** : 明確なWorkflowを指示せず、*目標*と*利用するであろうTool*だけClaudeに伝え処理させる方法。具体的なWorkflowがない時に有効

## Note/Tips

- Toolはシンプルで抽象的にすべし！
  - シンプルなToolを渡すことでClaudeは必要に応じて予期しない方法で賢くToolを使ってくれる

## Supplement

- 「抽象的なTool」の意味は、*Claude Code* のTool群との対比で捉えると分かりやすい。`bash` / `read` / `write` / `edit` / `glob` / `grep` といった汎用的なものだけを持ち、「refactor code」「install dependencies」のような専用Toolは持たない。専用Toolを増やすほど、開発者が想定した用途しか実行できなくなる。

- 抽象的なToolは単体では単純でも、Claudeが**連鎖させる**ことで複雑な要求に対応できる。例えば `get_current_datetime` / `add_duration_to_datetime` / `set_reminder` の3つがあれば、「11日後は何曜日？」は前2つの連鎖で処理できる。さらに情報が足りなければClaudeの側からUserに質問して補う。

- Agentsの柔軟性は**信頼性とコストとのトレードオフ**の上に成り立っている（詳細は後の章）。

## Reference

