# [What is a coding assistant?](https://anthropic.skilljar.com/claude-code-in-action/303235)

## Summary

- Coding Assistant のプロセスは人間同様以下のプロセスをたどる。
  1. 情報収集(Gather context)
  2. 計画立案
  3. 実装

- **tool use**: 言語モデルはテキストを受け取りテキストを返すことしかできない。Coding Assistantが言語モデルにツール利用を仲介することで、ファイル読み込みなど外界とのやり取りを可能にする仕組みが **tool use** である。
  - 具体的な内部処理は
    1. ユーザーのPromptを受け取る
    2. Coding AssitantはPromptを読み、必要なToolの利用指示をPromptに加える
    3. Language model はそれに対しCoding Assistantに対してActionを指示をする。(ex. ReadFile: main.go)
    4. Coding Assitantは実ファイルを読み、テキスト情報としてLanguage Modelに送る
    5. Language Modelは受け取った情報に基づいて最終的なResponseを返す

- Claudeはこの**tool use**t自体は全言語モデル共通の仕組みだが、Claudeはツールの役割理解・呼び出し判断・組み合わせ利用に特に長けており、それゆえ以下の恩恵が際立つ。
    - 問題解決能力の幅広さ(カスタマイズ性)
    - 基盤拡張性(既存プラットフォーム・ワークフローの流用性)
    - セキュリティ性
      - インデックス作成を必要とせず、外部サーバーに配置せず、つまりコードベースや資料をセキュアな状態のまま読んだり、編集したりできる。

### Note/Tips


## Supplement


## Reference

