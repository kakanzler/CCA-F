# [Skills](https://anthropic.skilljar.com/claude-code-101/469848)

## Summary

- skills : ユーザーのクエリに対し必要性が確認されたときに実行される処理
  - 名前と説明だけは毎回、必要性の確認のために読まれるが、CLAUDE.mdのように中身まで毎回読まれず必要なSkillのみ読み込まれるのでContext Windowを圧迫せずに済ませられる。
- 配置場所：
  - `~/.claude/skills/` : 個人設定。
  - `.claude/skills/` in Project repo :  バージョン管理することでチームメンバー全員に適用される

### Note/Tips

- skillを定義するタイミング
  - 同じ事をClaudeに指示していることに気づいたとき
    - ex : ブランドガイドラインに沿ってほしい、カラーやフォントをいつも指定している時、

- skillは特定の条件下で特定の処理をさせたいことを記載するのが望ましい。
  - 個人 : : コミットメッセージのフォーマット、ドキュメントの書式、コードの説明スタイルなど
  - Team : 会社のガイドラインに沿う、など

## Supplement（Claude Code CLIでのSkills）
  - skill.md の `description` がClaudeの起動判断の鍵。リクエストと各Skillのdescriptionを照合して合致したものを自動で発動する。
  - vs. CLAUDE.md : すべての会話で（中身まで）読み込まれ常時適用 ⇔ Skillは合致時のみオンデマンドで読み込まれる
  - vs. スラッシュコマンド : 入力（タイプ）が必須 ⇔ Skillは状況をClaudeが認識すると自動適用される

## Reference
