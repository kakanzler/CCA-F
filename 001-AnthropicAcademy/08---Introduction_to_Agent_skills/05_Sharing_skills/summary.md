# [Sharing skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434529)

## Summary

- `.claude/skills`にSkillsを登録し、Projectの管理対象としてチームで共有しましょう
- Plugin: teamやProjectでSkillを共有するための拡張機能を追加することでClaude Codeの拡張する方法。
- 管理者はmanaged settingsを通じてSkillを組織全体にデプロイでき、そのSkillは個人・Project・Pluginの同名Skillより最優先で実行される。加えて`managed-settings.json`に`strictKnownMarketplaces`を記載することで、Pluginをインストールできるmarketplaceのソースを制限できる（コンプライアンス要件を満たすため等に利用）。
- Built-inのSubagentとして*Explorer*,*Plan*,*Verify*などがあるが、これらはSkillsを利用することはない。Skillを利用できるのは`.claude/agents`に格納したSubagentだけであり、subagentにユーザーが明示的に利用するスキルを提示したとき、加えてMain Threadのように必要なタイミングではなくSubagent起動時に読み込まれる形での使用となる。
  - ここでのskillの指定は`.claude/agents/`下に配置されたsubagentの定義ファイルのfrontmatterにて、`skill: xxx, yyy`と指定する箇所があるのでそこでSkill名を指定する。

- `/agents`: custom subagentを作成する際に使用するコマンド

### Note/Tips

-  teamで共有するSkillsの例として、例えば「teamのコーディング規約」など。

- Pluginをつかうと`.claude`ディレクトリと同じような構成のディレクトリ`skills/`が作成される。これにより配信可能となる。
- またPluginを使うことで、Project特有のSkillをより汎化させた、コミュニティが使いやすいSkillを作ることができる

-  subagentが機能するコツとして、例えば「他のタスクとは独立した、固有のタスクについての処理を委任させる」など。

## Supplement

- `.claude/`は以下のようなツリーになっているが、これらすべてバージョン管理するべきである。

```
.claude/
├── skills/
│   ├── {SKILL_NAME}
│   │   ├── SKILL.md
│   │   ├── referece/
│   │   ├── scripts/
│   │   └── assets/
│   └── {SKILL_NAME}
│       └── SKILL.md
├── agents/
├── hooks/
├── commands/
└── settings/
```

## Reference

