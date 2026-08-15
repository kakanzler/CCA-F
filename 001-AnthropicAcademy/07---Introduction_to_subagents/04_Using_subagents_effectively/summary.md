# [Using subagents effectively](https://anthropic.skilljar.com/introduction-to-subagents/450701)

## Summary

- subagentsを使うタイミングかどうかはその中間的な情報の必要性、また分散処理できるタスクかどうかに大きく依存する
  - 中間情報があると、MainContextWindowが汚染されてしまうので結果だけほしいならSubagentを使うべき
  - subagent同士が互いに依存せず、親Agentがタスクを分散できる場合、有効だ。依存しあう場合、つまり subagentが他のsubagentに依存する場合、subagentをまたいだだけ情報が失われてしまう(要約の要約の要約、、のようになるため)。
- またフレッシュな視点でレビューなどの仕事を任せたいときもまた、Subagentが活躍するケースだ。

### Note/Tips

- Researchなどは典型的で、「どこにｘｘｘがある？」などの単発の質問についてはそれだけ回答を返せばよいのでSubagentに頼む典型例だ

- Reviewもよい典型。何度もClaudeとラリーした後、レビューを依頼しても、メインスレッドで続けてレビューをすると、それまで問題ない、と作成してきた先入観となってしまうため、レビューとしての信頼性は低い。そこでSubagentに委任することで、`git diff`によって得た情報とその差分からどうあるべきかを独自に判断でき、このフローをチームで共有することで一貫したレビュー体制を築ける。

- Custom System Promptを使ったSubagentの活用例
  - **Copywriting subagent** : 口調や話の構造を指定し、Subagentの要約にClaudeが最終的にどんな出力や話の構造で展開するべきかを組み込むことで、カスタマイズを可能に。
  - **Styling subagent** : subagent起動時に自動でDesign System fileを読み込ませることでCSSの書き方やコンポーネントのレイアウトの仕方などを前提に処理させることが可能



## Supplement

- subagentが機能しないものの例
  - *Expert Persona* : 無意味なcustom system promptの例
    - ”あなたはPythonのスペシャリストだ”というような文言はPromptに含めても意味がない。親Agentができず、Subagentにしかできるないとはない。
  - *Sequential pipeline* : 依存しているパターン
    - コーディングのsubagent
    - そのdebugのsubagent
    - bug fixのsubagent
  - *test runnners*: 中間情報が欲しいパターン
    - test失敗時、なぜ？どこで？テストが失敗したのかほしいが、agent返却時にその情報は失ってしまう。

- test runnerアンチパターンは、検証した全構成の中で最も成績が悪かった（performed worst among all configurations）と origin が明言している。



## Reference

