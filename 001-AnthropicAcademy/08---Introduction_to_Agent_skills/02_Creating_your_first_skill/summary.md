# [Creating your first skill](https://anthropic.skilljar.com/introduction-to-agent-skills/434527)

## Summary

- Skillはディレクトリ内の`SKILL.md`ファイルで構成され、frontmatterに`name`と`description`のメタデータを持つ。Claudeは起動時にこのメタデータのみを読み込み、リクエストとの意味的な適合性で使用是非を判断し、確認後にfrontmatter以降の指示本文を読み込んで従う。
- Skillの内容すべてをClaudeがロードする前に何をロードしようとしているかをClaudeがユーザーに利用を求める確認ステップがある
- Skillを読み込む際、異なるSkillの配置場所間で同名のSkillが存在した場合に読み込まれる優先度は **Enterprise** > **Personal** > **Project** > **Plugins**となる。Enterpirse(Anthoropicによって作成されたマネージドなSkill)に記載されたSkillが最も優先度が高くなる点に注意。
- 更新
  - 編集時：直接`SKILL.md`を修正し、Claude Codeを再起動する
  - 削除時：ディレクトリごと削除し、Claude Codeを再起動する

### Note/Tips

- skillの名前はなるべく競合しないようにUniqueに書くこと。
  - ex
    - review -> frontend-review

## Supplement

- 優先度の個所で言っているそれぞれは以下の通り.
  - Enterprise : Anthoropicが作成したマネージドなSkill
  - Personal : `~/.claude/skills/`下の個人のskill
  - Project : 対象のリポジトリに配置された`.claude/skills/`下のProjectが管理するskill
  - Plugins : installされているプラグイン

## Reference
