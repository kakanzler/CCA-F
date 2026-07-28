# [Roots walkthrough](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/295839)

## Summary

- `Roots`の実装手順
  1. `main.py`
    - main()内にて、まず引数としてアクセス可能なディレクトリを受け取り、`root_paths`という変数に代入する。
  2. `mcp_client.py`
     - `_create_roots()`というヘルパー関数を作成し、その中で
       1. Path(path).resolve()で名前解決し、Fullpathを取得し、
       2. **file://{p}**で該当のPathを*FileUrl*の型チェック(Pydantic)でチェックした者をfile_urlとし、roots(list)にmcp.types.RootというクラスのInstanceとしてuriとpath名前を紐づけてappendする。
  3. `mcp_client.py`
     - `mcp_client.py`ではすぐにRootのリストを送るのではなく、server側が必要になったタイミングでCallback関数にリクエストさせ非同期でRootを渡す。
     - `_handle_list_roots()`はserverに予約するcallback関数。
     - callback関数では`ListRootReuslt`インスタンスにrootsプロパティにrootをリストで指定する形で返す必要がある。
     - callback関数は`connect()`の`contextlib.AsyncExitStack._exit_stack.enter_async_context()`にて、`ClientSession()`にて、引数`list_roots_callback`でこのコールバック関数`_handle_list_roots()`を指定している。
  4. `mcp_server.py`
     - server側がファイルへのアクセスを試みる際は必ずclientのCallback関数を利用する。
     - Claude(LLM)がFileのFullpathを要する際は、Rootの一覧を取得する際にも、`@mcp.tool`で定義されたのこの関数をToolとして呼び出し、FullPathを取得する。
     - `Context.session.list_roots()`によって3の`ClientSession()`で定義されたセッション生成時に割り当てたコールバック関数でrootsを取得し、`ListRootsResult`オブジェクト内の要素`Root`を`core.utils.file_url_to_path`によって処理できるurlの形に変換し、それらをListとして返却している。
     - 該当部分
        ```python

        roots_result = await ctx.session.list_roots()
        client_roots = roots_result.roots

        return [file_url_to_path(root.uri) for root in client_roots]
        ```
  5. `mcp_server.py`
     - MCP SDKはToolがファイルを読もうとする際にこの範囲は読まない、などの制限することはないことに要注意。(前回も触れた)
      - *Security Boundary*を設定したい場合は、自身で受け取ったrootのリストが許可する範囲に含まれているかをチェックする`is_path_allowed()`のような関数を実装し、適切なタイミングで呼び出す必要がある。
        - `Context.session.list_roots()`によってrootのリストをコールバック関数で取得し、requestのあったURIを`core.utils.file_url_to_path()`で処理可能なURIの型に落とし込み、この範囲にあるかどうかを、`requested_path.relative_to(root_path)`でチェックしている。
        - 該当部分
            ```python
                roots_result = await ctx.session.list_roots()
                client_roots = roots_result.roots
                ...
                for root in client_roots:
                    root_path = file_url_to_path(root.uri)
                    try:
                        requested_path.relative_to(root_path)
                        return True
                    except ValueError:
                        continue

                return False
            ```
  6. `mcp_server.py`
     - この例では、`convert_video()`という`@mcp.tool()`で定義されたToolをCluadeが使用する際、input_fileを取得、Validateし、convert処理を走らせる前のタイミングでタイミングでis_path_allowedを呼び出し、問題があればValueErrorを返却する設計をしている。


### Note/Tips


## Supplement

- 実演回（walkthrough）のため、実装トレースは上記の核を押さえていれば十分。個別の手順詳細は origin 参照。


- `is_path_allowed()` は `relative_to()` の境界チェックの前に、以下の手順を踏んでいる。
  1. `requested_path.exists()` で存在確認
  2. 対象がファイルなら `.parent` でディレクトリへ丸めてから比較
  - root はディレクトリ単位の境界なので、ファイルパスをそのまま比較しないための処理。
- 前回（lesson 06 Roots）で「roots はクライアント側がサーバーへ公開するアクセス許可範囲」という概念は既出。本回はその概念のコード実装（client の生成・callback 登録、server の list_roots()/is_path_allowed()）に焦点。

## Reference

