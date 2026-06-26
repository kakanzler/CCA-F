# [Adding context](https://anthropic.skilljar.com/claude-code-in-action/303241)

## Summary

- Claudeは無関係なContext(FileやPrompt)が多すぎると効率が悪くなるため、必要な情報のみ与えることが重要である。
  - （Code BaseもすべてClaudeに与えればいいわけではない。）

- `/init` :
  1.  既存のコードベースをClaudeが以下を読み取る
    - Projectの目的・アーキテクチャ
    - 重要なコマンド・ファイル
    - コードの構造やコーディングスタイル
  2. Summaryを作成する
  3. `CLAUDE.md` にSummaryを記載する

- `CLAUDE.md` file
  - Claudeの推論をガイドするためのもので、Claudeは毎Queryこれを読む。
    - `/init` で作成したようなSummaryが記載される
    - 他に恣意的にClaudeに毎回する指示などを任意に設定可能

- ファイルの配置場所の種類(CLAUDE.mdの種類)
  - `CLAUDE.md`
    - `/init`で作成されるRepository直下のファイル。
    - Version管理の対象となり、チームメンバー全員で共有されるべきファイル
  - `CLAUDE.local.md`
    - `CLAUDE.md`同様Repository直下に自分で作成するファイル
    - これはVersion管理の対象とせず、自身の設定・指示を記載するファイル
  - `~/.claude/CLAUDE.md`
    - 自身のローカル開発環境におけるすべてのRepositoryに適用されるGrobalなファイル
    - 自身が関与するプロジェクトに適用させたい汎用的な指示を記載するファイル

- `@` : File mention
  - `CLAUDE.md`やPromptの中で特定のファイルをClaudeに参照させたい場合 `@ファイルのPATH`を記載する
  - 特に`CLAUDE.md`に記載すると、特別指示せずとも毎回参照するため、毎度適切なファイルを探して読み込むといった処理が軽減される。
  - 既に `AGENTS.md` がある場合は内容を複製せず、`CLAUDE.md` の1行目に `@AGENTS.md` と記載すれば先にその内容が読み込まれる。その下にClaude固有の指示を追記できる。

### Note/Tips
- Claudeに指示を追加したい場合
  1. `CLAUDE.md`に直接記載する
  1. `/memory`コマンドでClaudeに支持を記載させる

- `/memory`
  - 現在、自動読み込みがOn/Offになっているか確認可能
  - どの`CLAUDE.md`を読み込むかを手動で設定可能
  - `CLAUDE.md`に記載したのに反映されていなそう、と感じたときにちゃんと読み込まれてるか？を確認するのにまず実行するコマンド<sup> [1](#ref1)</sup>

## Supplement


## Reference
<a name="ref1"></a>
1． [Claude があなたのプロジェクトを記憶する方法 : /memory で表示および編集する](https://code.claude.com/docs/ja/memory#view-and-edit-with-%2Fmemory)