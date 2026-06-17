# Working with skills

## Summary

- **Skills** : 指示・スクリプト・リソースをまとめたフォルダーで、ClaudeがDynamicに読み込む「専門知識パッケージ」。特定タスクを毎回一定の手順で実行するために使う。
- 2種類のSkills:
  - **Anthropic built-in Skills** : Anthropicが作成・管理。Excel/Word/PowerPoint/PDF作成など。ユーザー操作不要で自動起動。
  - **Custom Skills** : ユーザーが自組織のワークフローや品質基準に合わせて作成するSkill。
- Claudeはユーザーのリクエストから文脈を判断し、適切なSkillを自動起動する（明示的な呼び出し不要）。
- **Projects vs. Skills**
  - Projects : 知識を蓄積する（what — 参照すべき情報）
  - Skills : 手順を定義する（how — 毎回同じステップで実行するプロセス）
  - 両者は補完関係：SkillがProjectの知識を参照することも可能。

### Note/Tips

- Skillは実行可能なコードを含むため、セキュリティに注意。Anthropic built-in Skillsは問題ないが、**外部ソースのCustom Skillは内容を確認してから使う**こと。
- Custom Skillの最も簡単な作り方：Claudeに会話形式で作らせる。伝えるべき情報は「何をさせたいか」「どんな時に使うか」、参考ファイル（テンプレート・スタイルガイド等）があればなお良い。
- ファイル操作時、ClaudeはChats上では元ファイルを直接編集するのでなく**新しいバージョンを生成**する。

## Supplement（Claude Code CLIでのSkills）

- claude.ai（ブラウザ版）はSettings > Capabilitiesで有効化する。
- Claude Code CLI（ターミナル版）は別の実装：`.claude/commands/{{skill_name}}.md`に登録することで`/{{skill_name}}`コマンドで呼び出せる。文脈からClaudeが自動判断して起動することもある。

## Reference

- [Working with skills](https://anthropic.skilljar.com/claude-101/383396)
