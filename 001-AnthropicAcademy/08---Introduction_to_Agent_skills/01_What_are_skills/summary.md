# [What are skills?]()

## Summary

- Skillは、`name`と`description`をfrontmatterに記載した`SKILL.md`ファイルを中心に、関連リソースをまとめた「フォルダ」として保存される。
  - Claudeはこの`description`を読み、promptの処理との適合性を確認し、適していれば利用する。
  - `description`は一行で書くこと

- `SKILL.md`の配置場所
  - `~/.claude/skills/下` : 個人の環境におけるすべてのリポジトリに有効化
  - `.claude/skills/下` : 対象のリポジトリに対し有効化。.gitignoreで指定しない限りはTeamに共有可能

- 比較
  - ClaudeがPromptの処理との適合性によって自動で読み込まれる。custom commandのように明示的に指定したり、`CLAUDE.md`のように毎回読み込まれるわけではない。
  - skillsは必要に応じて読み込まれるため、Context Windowを圧迫しすぎない点もメリットとしてある

### Note/Tips

- 特定の作業(コードのReview、コミットメッセージのフォーマット、会社方針の適用など)について何度も同じ指示をする場合、skillにすることでClaudeは正確なフローに沿って処理できる。

## Supplement

- skillが有効になっているかどうかはClaudeの処理ログをterminal上で確認することができる。

## Reference
