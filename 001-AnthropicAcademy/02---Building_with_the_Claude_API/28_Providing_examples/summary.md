# [Providing examples](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287746)

## Summary

- promptに入出力のペアを例として挿入する方法。指示で説明する代わりに実際の出力を見せる（tell ではなく show）ことで、*言葉にしづらい要求を伝える。*
  - **one-shot** : 例を1つだけ提示する方法
  - **multi-shot** : 例を複数提示する方法
    - 様々な特殊なケースを個別にカバーしたい場合や、有効なoutputが複数ある場合に有効

## Note/Tips

- 例を示すときは以下を意識する
  - XMLを使って、<sample-input> や <ideal-output>で囲う
  - 最もありがちな失敗ケースへの対処例を示す
  - 実際のタスクとの関連する例を示す
  - なぜそのOutputがよいのかと説明を加える

## Supplement

- 良い例をどこから調達するか、という観点がある。evalを回しているなら、**最高スコア（10点など）を取った出力をそのまま例として prompt に流用する**のが手っ取り早い。自分のタスクにおける「満点の出力」が何かを、Claudeに具体的に示せる。
- 例が効く典型は corner case（例: 皮肉を含むツイートの感情分析）。表面上はポジティブでも実際はネガティブ、といった素の指示では取りこぼす判断を、例を1つ足すだけで矯正できる。

## Reference

