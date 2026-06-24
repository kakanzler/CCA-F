# [The Explore → Plan → Code → Commit workflow](https://anthropic.skilljar.com/claude-code-101/469792)

## Summary

- Workflow :`Explore -> Plan -> Code -> Commit`とは。いきなりコードを書かせると後で軌道修正が増えるため、先に探索・計画して手戻りを減らすための型。
  - **Explore & Plan** :Plan modeではClaudeはファイルを編集できず読み取りのみ行う。コードを書く前のこの段階が最も軌道修正しやすい。
  - **Code** : Plan modeの計画に対し「Approve」を選択することで実際にClaudeがコーディングする。コーディング中ClaudeはじどうでTroubleShootingするが、ユーザーの介入が必要なこともある。
  - **Commit** : コミットする前にバイアスのない、第3者的な視点をもつsubagentにレビュー依頼することを推奨。その後、Claudeに自分のスタイルに沿ったコミットメッセージを生成させてpushする。

### Note/Tips

- パーミッションモードは`Shift + Tab`で切り替える。
- *Plan*で良い結果を得るためのポイント
  -  もし利用者に何かが必要になりそうかどうかの予測が立っているなら、それが必要かどうかも併せて具体的に記述すること
- コードを編集するつもりがなく、ただProject全体の構成が知りたいだけの場合であれば、Plan ModeにしなくてもSummaryを得ることは可能
- *Code*で良い結果を得るためのポイント
  - Plan時にPromptに目標達成の指標(Criteria)を含めること
  - Toolの利用も検討すること
    - これは後述されるClaude in Chromeなどの他のサービスや、Skills, Hools, MCPなども含まれ、これらを利用することでClaudeの精度・情報収集力向上が見込める
  - Test suite(テストで確認したい検証項目をまとめたものなど)をPromptに含めること
    - Claudeは具体的なテストケースなども作成可能
  - Claudeが同じような意図にそぐわない結果を返して、もし何度もそれに同じ修正指示をする必要が生まれたら`CLAUDE.md`に記載すること(08_the_claudemd_fileにて後述)

## Supplement


## Reference

