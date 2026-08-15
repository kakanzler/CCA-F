# [The StreamableHTTP transport](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296287)

## Summary

- **Streambale HTTP**: MCPのスタンダードなtransport方式
  - serverは公開サーバーで実装されることを想定している。
    - （同じマシン上での実装を前提としたSTDIOのtransport方式とは異なる）
  - Streamable HTTP はリモートHTTPサーバーに接続するためのtransportそのもの。その挙動を左右する設定として `stateless_http` / `json_response` の2つがあり、既定はどちらも `false`。
    - 制約
      - `stateless_http` : ステートレスな通信とする設定で、セッションを保持しない通信とする制御
      - `json_response`  : Responseフォーマットをjsonにするための制御
    - この2つを`true`にせざるを得ないデプロイ環境では、HTTPの制約を回避せずその内側で動作することになり、progress通知・logging・server起点のリクエストが使えなくなる。

- 標準的なHTTP接続だと、Client側が通常Server側にURLを知らせない為、以下の問題がある。
  - *問題*
    - Server側からClient側へリクエストを起こすことができない（server-initiated requestが成立しない）。
    - server側からの要求に応じたClientからの返却フォーマットが統一されていない
  - *影響*
    - server起点のリクエストが不可 ⇒ `Create Message Request`(sampling), `List Roots Request` が使えない。
    - 通知全般が不可 ⇒ Progress通知、Logging, 初期化完了通知、キャンセル通知など

### Note/Tips

- 重要なのはHTTP通信の際にはこういった制約が存在し、上記二つのキーの設定で対処はできるが、利用できなくなる機能が存在することを認識し、適切なケースに適切なtransportを選択する必要がある、ということを理解しておくこと。

## Supplement

- 標準的なHTTP接続でも以下の通信は可能。
    - Clientはいつでも初期化リクエストをServerに送信可能
    - Serverもそれに対して何に対してもResponse可能
- 実務上の切り分け指標: 「STDIOでローカル実行しているときは正常に動くのに、HTTPでデプロイすると壊れる」という症状が出た場合、まずこの2設定を疑うとよい（origin.mdが明示的に挙げている典型パターン）。

## Reference
