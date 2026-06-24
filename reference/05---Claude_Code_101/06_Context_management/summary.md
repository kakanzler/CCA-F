# [Context Management](https://anthropic.skilljar.com/claude-code-101/469793)

## Summary

- Context Managementは Claude にとって非常に重要な概念
- Context Window : Claudeが保持できる記憶領域(メモリ)で、ユーザーのクエリ、クエリで出力した結果、Toolを利用した場合はその際の入出力もすべて保持し続ける。
- Context Windowが限界に達したとき、ClaudeはAutoで `/compact`を実行する。コマンドの実行によりClaudeは要点をまとめ、その過程で不要と判断された細部の情報は失われるので注意。
- Command: 手動で以下の操作が可能。
  - `/compact`
    - 保持しているすべてのコンテキストを要点にまとめるコマンド
    - Context Windowの限界まで占有してきているが、まだClaudeと引き続き現在の会話を要するときに使用する。
  - `/clear`
    - コンテキストをすべて消し、まっさらな状態から始める際に使うコマンド
    - これまでの会話との依存性を排除し、新しい文脈で会話したいときに使用する。
    - ただし、セッションをまたいで Claude に覚えておいてほしいことは `CLAUDE.md` に記載しておくと、毎回ゼロから再発見せずに済む。
  - `/context`
    - 現在のコンテキストの占有状況を視覚的に確認するコマンド
    - Context消費状況を確認するタイミングで使用する。また、何がContextWindowの多くを占めているのかなどの分析にも使用する。

### Note/Tips

- プロンプトは具体的に書いて指示するべし。曖昧な指示はその内容理解にClaudeはその分のContextを消費する。
- MCP Serverは関連づいているだけでContext Windowを占有するため、不要な連携は無効化するべし。または、必要なときだけ読み込まれる「Skills」を MCP Server の代替として検討するとよい。
- Subagentはそれぞれが独立したContext Windowをもち、Responseを作成するにあたって分割した処理に対してSubangetがまとめた内容をAgentがまとめ上げるので、結果だけほしい場合(つまり結果を得る過程で得る微細な状況は不要の場合)はContext Windowを効率的に使うことができる。Subagentを使うべし。

## Supplement


## Reference

