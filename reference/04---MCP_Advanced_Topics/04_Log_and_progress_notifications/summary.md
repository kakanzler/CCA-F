# [Log and progress notifications](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296284)

## Summary

- Logging
  - *用途*
    - (重要) 長い処理において、ユーザーへ何を処理している最中なのかを知らせる
    - (重要) いつ処理が終わりそうかをユーザーへ伝える
  - *実装*
    - *Server*
      - 該当の`mcp.tool`で定義されたメソッド内を非同期に設計し、以下を記載する。
        - ログメッセージ：`context.info(str)`
        - プログレスバー: `context.report_progress(現在の進捗:int、全体: int)`
    - *Client*
      - serverから非同期に送付される情報をcallback関数をserverに予約して実行する必要がある。それぞれ以下
      - `ClientSession(logging_callback=...)`
      - `ClientSession.call_tool(progress_callback=...)`

### Note/Tips

- Loggingの利用方法
  - CLI : そのままTerminalにlogの表示、Progressの表示
  - Web APP: WebSocketsやPollingを利用したブラウザの更新
  - Desktop App: 自身のUIにカスタマイズしたlog表示、Progress表示

## Supplement

- loggingは純粋にUXを高めるための手段なので絶対必要なものではない、オプションに過ぎない。が、その効果は高い。

- Context は自分で生成するものではなく、`context: Context` をキーワード専用引数（`*,` の後ろ）に宣言すると SDK が実行時に自動注入する。
- callback は server 側ではなく client 側で登録する点に注意。`logging_callback` は ClientSession 生成時に一度、`progress_callback` は call_tool ごとに指定する（＝ログはセッション単位、進捗はツール呼び出し単位で扱い分けられる）。server は通知を送るだけで、受け取って表示するかどうかは client の責務。

## Reference

