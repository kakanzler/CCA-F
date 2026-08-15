# [Configuration and multi-file skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434526)

## Summary

- Frontmatter
  - `name` (必須): 英語小文字、数字、ハイフンのみを使ってSkillの内容を簡潔に(最大64文字)表した名前。ディレクトリ名と一致している必要あり。
  - `description` (必須): Claudeがこのスキルをいつ使うべきか、このSkillがなにをするかを最大1024文字で記載する
  - `allowed-tools` (オプション): このスキルが有効な際にClaudeがどのToolを使用できるかを制限する
  - `model` (オプション): このスキルを使用する際にどのモデル名を使用するべきか明記する

- `allowed-tools`を利用することでSkill使用時にToolの制限を設定できる。
- `SKILL.md`は長くても500行に留め、必要に応じてClaudeが参照できるように、`skills/{SKILL_NAME}/reference/`, `skills/{SKILL_NAME}/scripts/`, `skills/{SKILL_NAME}/assets/`に参考情報を配置するとClaudeは段階的に情報を得るので必要以上にContext Windowを圧迫しないようになる(= Progressive Disclosure)
- `skills/{SKILL_NAME}/scripts/`下に配置するscirptsはContextWindowにロードされずに実行されるように記載されるべきだ。`SKILL.md`ではそのscriptsをContext Windowに読めとClaudeに指示せずそのScriptsを実行しろと記載することで、入力にはトークンを消費せず、出力のみトークンを消費するので効率がいい。非常に重要なポイント。

### Note/Tips

- `allowed-tools`の利用例
  - `Read`, `Grep`, `Glob`, `Bash`を明示的に許可した読み取り専用のスキル。

- progressive disclosureについて
  - 以下のように配置し、`SKILL.md`内でいつ、なんの処理でそれぞれどうかかわるのか明記して紐づける
    - `skills/{SKILL_NAME}/scripts/` : 実行可能なコードを配置する場所
    - `skills/{SKILL_NAME}/reference/` : 追加のドキュメントを配置する場所
    - `skills/{SKILL_NAME}/assets/` : 画像ファイルやテンプレートなど他ファイルを配置する場所

## Supplement

- `description`はClaudeがSkillを起動するかどうかのマッチングに使う唯一の判断材料であるため、必須フィールドの中でも最も重要とされている。

- `allowed-tools`を記載しない場合のデフォルトの仕様として、Claudeはすべての操作が可能である。

- `skills/{SKILL_NAME}/scripts/`を効果的に使うケース
  - 環境のValidation
  - 一貫性が必要なデータ変換
  - 生成コードよりテスト済みコードの方が信頼できる処理（毎回Claudeに書かせるより一貫して動くスクリプトを実行させたい場面）

## Reference

