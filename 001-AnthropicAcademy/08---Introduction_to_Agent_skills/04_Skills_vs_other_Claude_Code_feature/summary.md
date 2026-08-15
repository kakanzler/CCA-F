# [Skills vs. other Claude Code features](https://anthropic.skilljar.com/introduction-to-agent-skills/434528)

## Summary

- Claude Codeが提供するそれぞれのカスタム可能な機能を効果的に活用するべし

- まとめ

| vs  | **Skills**|
|---|---|
|`CLAUDE.md`  | - `CLAUDE.md`: すべての会話の度に読まれるので、Projectの標準などのベースラインを記載するのに使うのに適している。<br>- **Skills**: ClaudeがPromptから必要性を判断し、それに応じて読まれるので、特定のタスクについて特記したり、その時だけ必要な知識を挿入するのに適している。|
| *Subagents* |- *Subagents*: Main Threadとは独立してContext Windowを持つので結果だけ得たい、分散処理可能なタスクの処理に適している。<br>- **Skills**: Main Contextに特定のタスクについての処理方法を与える。|
| *Hooks* |- *Hooks*: ユーザーが指定する特定のタイミングでのイベント駆動の処理に適しており、自動で必ず実行される。<br>- **Skills**: プロンプト駆動であり、利用是非はClaudeがDescriptionを読み込み判断する。|
| *MCP Servers* |- *MCP Servers*: 外部ツールとの統合を提供する。<br>- **Skills**: 比較対象ではない。|



### Note/Tips

|   | 使用ケース/例 |
|---|---|
|`CLAUDE.md`  | - Project全体に広く適用できる標準的ルールを記載したいケース <br>---> 絶対に禁止したい処理事項(DBの編集) <br>    ---> コーディング規約や利用するFrameWorkの好みの設定<br>|
| *Subagents* |- Main ThreadのContext Windowとは切り離してタスクを別で処理したいケース <br> - Main Threadの会話からそれたツールを実行したいケース  |
| *Hooks* |- ファイルを保存したタイミングで必ず実行したいケース <br> - 特定のツールを呼び出した際にValidationを行いたい場合 <br> - Claudeが何かを実行したタイミングでの自動化処理をinsertしたいケース |
| *MCP Servers* |- 外部ツールを利用したいケース|
| **Skills** |- 特定のタスクに関して決まった処理を実行させたいケース <br> - 毎回読み込むには重すぎるが必要なときには知っておく必要のある詳細な情報を現在の会話（Main Thread）に挿入したいケース <br> - Claudeの推論に必要な指針を記載したいケース |

## Supplement

- すべてをSkillsで処理しようというようなことはすべきではなく、適材適所なツールを複合的に使うことが推奨される


## Reference

