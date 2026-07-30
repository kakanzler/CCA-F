# [JSON message types](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296290)

## Summary

- MCP は client - server間のすべての通信はJSONで行われる。
  - 通信内容は以下の2パターンに分類される。これはClient→Server / Server→Clientどちらの方向のメッセージにも共通する分類である。
    1. Request-Result Messages
       - Pairになるのが特徴
         - 例
           - ツール呼び出し (`Call Tool Request` / `Call Tool Result`)
           - 利用可能な情報の一覧取得 (`List Prompts Request` / `List Prompt Result`)
           - 利用可能な情報から中身を読み取る(`Read Resource Request` / `Read Resource Result`)
           - 初期化要求 (`Initialize Request` / `Initialize Result`)
    2. Nortification Messages
       - 一方向の通知の送信でResponseを待たないRequest
         - 例
           - Progress Barなどに用いられる作業の進捗情報の通知
           - loggingのメッセージ送信
           - 利用可能なToolの中身が変更された際の通知
           - Resourceの中身が修正されたりして更新された際の通知
- MCP仕様書(Reference参照)には以下2つの役割分担が記されている。大切なのは必要に応じて双方向に通信されるということ。
  - *Client Message* : ClientがServerへ送信する要求(Toolの要求など)や通知(Client→Serverもある)
  - *Server Message* : ServerがClientへの要求(異なる通信メソッドが必要な時など)または通知(Loggingなど)

### Note/Tips


## Supplement

- MCPを作成したのもAnthropicで2024年11月にOpensource化し、Referenceに書いたAuthoritative SourceもAnthropicが作成した規格なんだな。
- つまり、ReferenceのGitHubは一時情報であり、この講座も信頼のおける情報と考えていいわけだ。

- 規格がTypeScriptで記載されているのは構造や型を明示的に記載できるから使用されている。(TSを使えということではない。)

- Server→Client のメッセージがあることを理解しておくのが重要なのは、transport（特に streamable HTTP transport）によって「どの向きに・どの種類のメッセージを流せるか」に制約があるため。用途に応じて正しい transport を選ぶ判断に直結する。


## Reference

- [MCP specificaiton](https://github.com/modelcontextprotocol/modelcontextprotocol)
  - MCP client, sereverの仕様が定義されている
  - TypeScriptによって、すべての有効なメッセージ(Call Tool Request, Call Tool Resultなど)が定義されている。