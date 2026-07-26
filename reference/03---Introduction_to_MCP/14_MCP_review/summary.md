# [MCP review]()

## Summary

- MCP serverの基本要素
  - *Tool*
    - 制御主体： Model(ClaudeでいえばOpusなどのLLM)
    - 特徴：
      - ClaudeがタスクをこなすのにClaudeがToolの使用をPromptから必要性を自動で判断して使われる
    - 作成タイミング
      - Claude自身が新しい処理方法などを要するとき
  - *Resource*
    - 制御主体： Application
    - 特徴： Application内で、いつ外部データをFetch(最新情報を取得)し、利用するべきかを判断する。(よくあるのはUIの要素や会話におけるContextを挿入するため)
    - 作成タイミング
      - UIやContextのためにApplicationに情報を取得したいとき
  - *Prompts*
    - 制御主体： User
    - 特徴：
      - ボタンの押下やメニューでの選択、`/`コマンドなどにより事前に調整されたpromptを実行する。
      - Promptはユーザーの要求に応じた洗練されたPromptを実行することになる。
      - ClaudeのUIではChat下部のボタン操作がこのPromptで実装されているらしい。
    - 作成タイミング
      - 事前に定義したPromptをユーザーに使わせたいとき。

### Note/Tips


## Supplement

- Resourceの例：ClaudeのUIにある"GoogleDriveから追加する機能"は裏側の処理では、どのDocumentを見せるべきかを決定し、Contextを追加処理をする機能となっている

## Reference

