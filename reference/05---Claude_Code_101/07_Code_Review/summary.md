# [Code Review](https://anthropic.skilljar.com/claude-code-101/469794)

## Summary


- プルリクする前にClaudeにSubagentが起動し、Biasのない状態でCodeをレビューさせることができる。ただし、Subagentはread onlyの権限でレビューさせるのがポイント。
- またCommandにはBuilt-inが用意されている。:
  - `/commit-push-pr` skill : コミット -> プッシュ -> プルリクを一貫して実施してくれるスキル
  - `claude --from-pr <PR number>` : `gh pr create`で作成したPRにはセッションが自動で紐づく。後日レビュー対応やビルド修正のため、中断したセッションを途中から再開するコマンド

### Note/Tips


## Supplement


## Reference

