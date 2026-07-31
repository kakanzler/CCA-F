# [The STDIO transport](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296291)

## Summary

- JSON メッセージを実際に運ぶ通信路を transport と呼び、その実装は STDIO・HTTP など複数ある。

- STDIO通信
  - *概説*
    - clientのsubprocessとしてserverを立ち上げ、標準入出力(STDIO)を利用しclient-server間通信する、単純なtransport．
      - MCP server : `stdin` でClientからの入力を受け付け
      - MCP server : `stdout` でClientへ出力する
    - serverとclientが同一マシンにあるときのみ適している方法

  - *実装*
    - `uv run server.py`でserverを起動すると、STDIOの入出力を利用できる形で起動される。
  - *シーケンス例*
      ```mermaid
      sequenceDiagram
          MCP Client ->> MCP Server : Initialize Request
          MCP Server -->> MCP Client : Initialize Result
          MCP Client ->> MCP Server : Initialized Notification
      ```
    - MCP 接続に必須の3メッセージのハンドシェイク
      - まずClientとServerの通信の第一声は`Initialize Request` / `Initialize Result`
      - そして通信を行う。ここでは `Initialized Notification` というMessageにより、初期化完了の通知を送るという初期化処理をしている。
      - これにより`Tool Call Request`など他のメッセージが処理できるようになる。

- どんな通信手段であっても以下4パターンに大別可能
  1. Client -> Server(stdin) request
  2. Server(stdout) -->> Client response
  3. Server(stdout) -> Client request
  4. Client -->> Server(stdin) response

### Note/Tips

- stdio通信は(いつでも通信できるため)理想的な双方向通信である。
  - ゆえに、HTTPなど他の通信への理解を深めるためのベースラインでもあるから重要。
  - またテストや開発時のデバッグなどにも有効。
  - stdio を"全部できる理想形"として覚えておくと、 逆に他 transport は「そこから何が削られているか」という視点で理解を進められる。


## Supplement

- messageが以下に2分されるのは前回の講座でやったので割愛
  - Request-Result Messages
  - Notification Messages

- `uv run server.py` で起動したserverは stdin を読み stdout に書くだけなので、クライアントを別途書かなくてもターミナルに JSON を直接貼り付けて応答を確認できる。

## Reference

