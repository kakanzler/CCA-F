# [Prompt evaluation](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287731)

## Summary

- **Prompt engineering** : よいPromptを書くためのテクニック
  - よい ≒ ClaudeがUserの何を要求しているか、どう返却してほしいかを理解しやすい、
- **Prompt evaluation** : Promptがどれくらい実際に機能しているのかを自動で測る手法
  - 例
    - 期待する答えを用意し、それと照合してテストする
    - 同じ内容だが別の聞き方で結果を比較する
    - エラー出力のレビューする
  - 開発フローが以下のように改善される
    1. 本番前のProptの弱さを特定
    2. 異なるPromptを用いた客観的な比較
    3. 定量的な改善を軸に自信をもって行われる評価・改善サイクル
    4. より信頼できるAIアプリを作成

- promptの草案を作成した後は*evaluation pipeline*に通しましょう。
  - Userの予期しない入力により本番で壊れてしまうリスクを避けるため。

## Note/Tips


## Supplement

- 数個の特殊なケースで十分と判断しがちだが、多くの場合下に見積もりすぎており、予想だにしない入力がなされる。
- evaluation pipeline は無条件に優れた選択肢ではなく、テスト基盤の構築という先行投資（工数・コスト）と引き換えに信頼性を得るトレードオフ。手軽な「数回叩いて調整」に流れてしまうのは、この初期コストが理由。
- 「本番で壊れてから直す」のではなく「開発中に問題を捕まえる」ことが evaluation の目的であり、prompt engineering と対立するものではなく補完関係にある（書く技術と測る技術）。

## Reference

