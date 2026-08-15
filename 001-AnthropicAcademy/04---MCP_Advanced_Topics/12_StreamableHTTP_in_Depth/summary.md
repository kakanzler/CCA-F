# [StreamableHTTP in depth](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296286)

## Summary

- **StreamableHTTP**: 通常のHTTP通信では難しい`Server ->> Client`へのRequestを *SSE(Server-Sent Events)* で解決する通信方法
  - Flow
    ```mermaid

    sequenceDiagram
    participant A as MCP Client
    participant B as MCP Server

        note over A, B: 0. Initialization

        A ->> B : Initialize Request
        B -->> A : Initialize Result
        note left of B: Request Headers {mcp-session-id : s001}
        A ->> B : Initialized Notification
        note right of A: Request Headers {mcp-session-id : s001}

        note over A, B: 1. After initialization

        A ->> B : [GET] mcp-server.com/mcp/
        note right of A: Request Headers {mcp-session-id : s001}
        B -->> A : ** SSE Response **

        note over A, B: 2. Request from Server to Client
        B ->> A : ** SSE Response **

        note over A, B: 3. Call Tool Request
        A ->> B : [POST] mcp-server.com/mcp/
        note right of A: Request Headers {mcp-session-id : s001}
        B -->> A : ** SSE Response **

    ```

  - 初期化のタイミングでServer側が払いだした`mcp-session-id`(@`Initialize Result`)を以降の通信のRequest Headerに含めることによって、通信の一意性を担保しており、以降はこのidをHeaderに含め通信し、Serverからは**SSE**によりResponseを返す。これで通常のHTTPではできなかった *Server - Client間の通信* を実現している。
  - SSEは2つに大別される(**Dual SSE**) :
    - **Primary SSE**: メインのSSE。 初期化後、無期限にOpen状態を維持する接続。
      - *Progress Notification*
    - **Tool-Specific SSE**: Tool呼び出し時の接続方法。Tool呼び出し時にSSEを別途作成し、Toolの結果送信時に自動で閉じる接続となる。
      - *Logging*, *Tool Call Result*

- 初期化後は全リクエストに session id を付与しなければならない。一方で、Primary / Tool-Specific という複数のSSE接続の張り分けと破棄はシステムが自動で管理してくれる。

### Note/Tips

- ServerからはHeaderを指定しない。`mcp_session_id`のSSE Responseとして返却する形でRequestしているのがポイントと言えそう。
- LoggingはProgress NotificationとちかいからPrimary SSEかとおもいきやTool-Specific SSEらしい。
- `stateless_http`, `json_response`は基本的に`False`に設定する必要がある。用途によっては`True`にする必要が生まれるがSSEは壊れる。詳細は前項11を参照。

## Supplement

- HTTPがそもそも *Client ->> Server* のために設計されている。(その逆ではない)

- `mcp-session-id` は Client が生成するのではなく、Server が `Initialize Result` のヘッダで払い出す。Note の「ServerからはHeaderを指定しない」が成り立つのは初期化*後*の話で、初回だけは Server 側がヘッダを付ける。

- Tool Call Request 自体は SSE ではなく POST で Tool-Specific SSEではない。 Tool Call Response は Tool Specific SSE。

## Reference

