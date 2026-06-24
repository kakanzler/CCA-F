# [Subagents](https://anthropic.skilljar.com/claude-code-101/469796)

## Summary
- claudeはSubagentにタスクを分割して分散処理することが可能で、Subangetはそれぞれ独立したContext WindowをもちContext効率良く、つまり、Subagentは分割したタスクごとに最小限のContext Windowで情報をClaudeに伝えるため、C;audeはContext Rotを回避しつつSubagentが作成した要点を統合しユーザーへの応答を生成できる

- subagentは`/agents`から対話的に作成する
  - その後、ClaudeはそれぞれのSubagentに対して、名前や説明、Subagent向けのPromptを生成する。この説明はユーザーのプロンプトに応じてClaudeがどのタイミングでsubagentを呼び出すかの判断材料にもなる。

### Note/Tips

- `Persistent memory`: 
  - Subagentに永続的にメモリを保持させることが可能で、継続的に同様のSubagentを同プロジェクト内で利用する際に便利
- `Preload skill`: 
  - Subagentに`skill`キーを追加、`skill`名の一覧を作成することでSubagentにskillをあらかじめロードさせることが可能。ただし、メインでつかうようなsSkillとはことなり、すべてのスキルがロードされることに注意。

## Supplement

- Context window : 言語モデルが応答を生成する際に参照するすべてのテキスト(応答含む)を指す。モデルの「作業メモリ」を表す。 <sup> [1](#ref1)</sup>
- Context rot (コンテキストの劣化) : Context Windowが大きければ大きいほど複雑で長いプロンプトを処理できるが、精度が落ちることが知られている。 <sup> [1](#ref1)</sup>
 
## Reference

<a name="ref1"></a>
1. [コンテキストウィンドウ](https://platform.claude.com/docs/ja/build-with-claude/context-windows)