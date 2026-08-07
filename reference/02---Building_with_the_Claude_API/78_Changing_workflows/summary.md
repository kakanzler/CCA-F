# [Chaining workflows](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287800)

## Summary

- **Chaining workflows** : 巨大な、複数の処理をもつ１つの要求をSequentialなSubtaskに分割し１Stepずつ推論させる方法。
  - Stepの合間にClaudeに依らない処理を挿入するFlowもつくれる
  - Claudeは一つの観点に集中して推論するので正確な推論がしやすい

## Note/Tips

- 並列に分割できないタスクでも直列に分割することでClaudeのPerformanceは向上するということ。
- 長文のPromptをChaining Workflowにするための実用的な手順は以下。
  1. まずはその長文のPromptをClaudeに送信する。
  2. Claudeからは十分な要件を満たす回答は得られないだろうが、これでよく、
  3. その回答について、どのように修正するべきかをClaudeに要求する。
  4. Claudeは初回の回答の修正タスクとして集中できる。

- 有効な場面
  - 複数の要件を満たす必要のある複雑なタスク
  - ステップに応じた処理やValidateが必要なタスク
  - 長文のPromptだとClaudeが一部の制約を無視してしまうタスク


## Supplement

- Chainingは追加の依頼をするようなもので、結果をよりよく改善していくフロー。

## Reference

