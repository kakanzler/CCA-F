# [Notifications walkthrough](http://anthropic.skilljar.com/model-context-protocol-advanced-topics/291036)

## Summary

- loggingの実装
  1. *Server*
     - `@mcp.tool()`で定義されるメソッドは`ctx : Context`を引数として受け取り、logging, progressの送信にはこれを用いる。
  2. *Server*
     - `@mcp.tool()`で定義されたメソッド内で、`ctx`を用いて、以下の通り出力できる
       - `ctx.info()` : 警告でもエラーでもない、本番でも出力するログ送付
       - `ctx.warning()` : 警告としてのログ送付
       - `ctx.debug()` : 開発時のみ送付するデバッグ目的のログ送付
       - `ctx.error()` : エラーとしてのログ送付
       - `ctx.report_progress()` : 進捗状況の送付。(※進捗度合いはユーザーが任意に定める。)
  3. *Client*
     - ServerにRequestする際にこのメソッドに返却してくれ、とcallback関数を予約する必要がある。ここでは、log用の`logging_callback()`, Progress用の`print_progress_callback()`を定義している。
       - *logging*
         - 引数はparams。 `params.data`にログのテキスト情報がある
       - *progress*
         - 引数としてprogress(float), total(float), message(str)を引き受けられ、total, messageはオプションとしている、がここは設計による。
  4. *Client*
     - 用意したCallbackを登録する。
       - *Logging*
         - `ClientSession()`でSession生成タイミングで引数`logging_callback`(+ 標準入出力のreadとwrite)を指定する。
       - *progress*
         - セッションごとに`ClientSession.call_tool()`で引数`progress_callback`を指定する。

### Note/Tips


## Supplement

- この回は lesson 04（Log and progress notifications）の概念を実装で追う実演回。概念の核（通知の用途 / callback は client 側で登録 / logging はセッション単位・progress は呼び出し単位）は lesson 04 済みなので、詳細は実演ベースとして origin 参照。
- `ctx.info()` / `ctx.report_progress()` は coroutine なので `await` が必須。ゆえに `@mcp.tool()` のメソッドは `async def` で定義する必要がある（origin の `add()` も `async`、`asyncio.sleep(2)` は長時間処理の模擬）。

## Reference

