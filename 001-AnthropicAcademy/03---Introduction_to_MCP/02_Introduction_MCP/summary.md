# [Introducing MCP](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296689)

## Summary

- MCP(Model Context Protocol) server: 外部ツールとの間をつなぐインターフェース
  - 大まかな流れ
    - clientがMCP serverへアクセスし、ツールやプロンプトを使って、外部サービス(ブラウザ, DB, GitHubなどのサードパーティサービス、他)の処理をする。
  - MCP Serverのインターフェースは以下の3つで構成されることが標準化されている。
    - toolds
      - ex. `get_repos()` (APIのような形で提供されている)
    - prompts
    - resources

    ```mermaid
    graph TD;
        A[MCP Client <br> @our server] -- connecting --> B[ tools, prompt, resources <br>@MCP server];
        subgraph Outside
            B --> C[Outside Service];
        end
    ```

   - 意義
     - 外部ツールとのインターフェースをユーザーが一から作る必要がないこと
     - 処理したい対象（GitHub等）のtool schemaがMCP server側にあらかじめ定義・提供されており、自分で実装しなくてよいこと


### Note/Tips

## Supplement

- MCP serverはだれが作るものか
  - AWSやGitHubはOfficialに自身のサービスに対するMCPサーバーを作成・提供している。
  - 自身でMCPサーバーを作成することも可能

- GitHubにはいろんな機能がある。それを一つ一つ自身でインターフェースを作成・テスト・保守するのは骨が折れる。それを提供してくれるのがMCP。

- APIを呼ぶのと何が違うのか？
  - APIを呼ぶ場合、様々なAPIをコールして自身の処理の一連の流れ(tool schema)を自身で構成するが MCPサーバーではそのtool schema/関数があらかじめ定義・提供されているので、自分で書かなくてよい

- Toolとの違い
  - MCPはすでにtoolが作成されている状態でMCPに対してPromptを投げtool schemaを介してtoolを利用するが、いわゆるtool(Grep, Glob, Write, Editなど)はClaudeによる操作の話なので全く別物を指している

## Reference

