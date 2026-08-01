# [State and the StreamableHTTP transport](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296285)

## Summary

- *スケーリング時の問題点*
  - MCP Clientが増え、MCP Serverが大量のTrificを処理する必要が生まれた場合、スケーリングのためLoadBalancerを介した通信をする必要性が生まれる。しかし、前項で扱ったように、Dual SSEで維持した通信経路を固定しsession_idをHeaderに含めて通信する必要性がある。

- *解決策*
  - `stateless_http = True` :
    - *when to use?*
      - MCP ServerがLoadBalancerなどで水平負荷分散したいとき
    - *why this is valid?*
      - Clientは初期化をするための最初のハンドシェイクが必要なくなり、ClientはServerに直接Requestできるようになる、つまり、どのServerへLoadBalancerが振り分けてもstatelessなResponseで十分となるから。
    - *trade-off*:
      - Clientは`session_id`を取得できなくなり、ServerはClientの通信を維持しようとしなくなり、サーバーからClientへの要求ができなくなり、以下が不可になる。
        - Sampling
        - Progress Notification
        - Subscriptions(リソースのUpdateなど)
  - `json_response = True` :
    - *when to use?*
      - 途中経過が不要で、最終結果のJSONだけ受け取れればよいとき
    - *why this is valid?*
      - POST応答が「SSEストリーム」ではなく「普通のJSONレスポンス1発」になるため、SSEをパースできない一般的なHTTPクライアントやプロキシとそのまま連携できるから。
    - *trade-off*:
      - POSTに対する返信用のStreaming処理ができなくなる。つまり**SSE Response**ができなくなるので、以下が不可になる。
        - 実行中のProgress Notification
        - 実行中のLog送信
        - 最終的な出力以外の出力

### Note/Tips

- 実際の設定場所
    ```python
    mcp = FastMCP(
        "mcp-server",
        stateless_http=True,
        json_response=True
    )
    ```
  - `stateless_http` と `json_response` は独立したフラグで、片方だけ有効にできる。

- 開発段階ではLocalのSTDIOで実装しているが、製品版ではHTTPを検討しているProjectがあるなら、開発段階でHTTPなどを試すほうが良い。開発中に問題が見つかるほうがマシだから。

## Supplement

- 単純にLoadBalancerを扱うと、Balancingのために、Clientが張る2本の接続（GET SSE と POST）が別インスタンスに振り分けられうることが問題の核心
  - tool内でSamplingを使う場合、POSTを受けたServerが、SSE接続を保持している別のServerに依頼しなければならず、Server間協調が必要になる。`stateless_http=True` はこの協調問題そのものを消す（＝Server -> Client方向を諦めるということ）。

- `json_response` は「POST応答をSSEストリームで返すか、単一のJSONで返すか」という応答形式の話であり、sessionを持つ/持たないという軸とは別物。

- Streaming不可 = POST への応答が text/event-stream（SSE）ではなく application/json の単一ボディになる

## Reference

