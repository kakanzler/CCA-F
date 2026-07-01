# [What are subagents?](https://anthropic.skilljar.com/introduction-to-subagents/450698)

## Summary

- SubagentsはClaude Codeから呼び出される、まさに部下のようなものでそれぞれが自身のContext Windowをもち、それぞれに割り振られた特定のタスクをこなし、その結果を簡潔な要約としてClaude Codeは受け取るため、その中間情報(要約を得るまでに利用した情報)は大元のClaude Codeは受け取らない為、Context Windowは余計な情報で汚染されない

- Subagentsは親Agentから受領するもの
  1. Configファイルに記載したSubagentの役割・振る舞いの定義(Custom system prompt)
  2. ユーザーのpromptに基づいて親Agentが作成したサブタスクの定義

- Subagentのライフサイクル
  1. 受領した情報をもとに自身でサブタスクを解決
  2. 要約を親Agentに返却
  3. 消去

- Claude Code に標準搭載されたSubagent
  - **General Purpose subagent** : 探索と実行の両方を複数ステップで実行できるsubagent
  - **Explore** : コードベースを高速に検索し、ユーザーの意図に応じてどこを見ればいいのかを提示してくれるsubagent
  - **Plan** : Planモード中にコードベースを分析・研究するためのsubagent(Planモード時すでに使っている)

- Custom Subagent
  - もちろん可能。詳細は別途

### Note/Tips

- 親Agentは要約のみ受け取るのでその過程でSubagentがどのようにその結果にたどり着いたかは追跡できないことに注意。

## Supplement

- Context Windowをきれいな状態に保つということはつまり、 より長いセッションが可能で、効率的なアウトプットが期待できるということ

## Reference

