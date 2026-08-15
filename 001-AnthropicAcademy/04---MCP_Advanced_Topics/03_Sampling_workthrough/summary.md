# [Sampling walkthrough](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/295172)

## Summary

- samplingの実装方法
  1. *Server*
    - `context.session.create_message()`を使用し、LLMへのメッセージを作っている。このメソッドの内部で引数messagesにSamplingMessage()のリストを渡しているため、Client側でSamplingとして処理される。
  2. *Client*
    - `sampling_callback()` の第2引数 `params` (CreateMessageRequestParams型) に Serverから受け取ったメッセージのリスト(params.messages)が入っており、それをLLMへ渡している。
  3. *Client*
    - MCP Serverから受領したメッセージはしばしばLLMへ互換性があるフォーマットへ変換する必要性が生まれるため、ここでは`chat()`にて変換を行っている。(roleが"user", "assistant"以外を排除している。)
  4. *Client*
    - LLMで作成されたテキストを`CreateMessageResult`メソッドをつかってServerに返却する。
  5. *Client*
    - `ClientSession` の引数 sampling_callback に、実装したコールバック関数を登録する。これを忘れるとSamplingが起動しない。
  6. *Server.py*
    - 受け取った情報をタスクに応じて任意に処理する。

### Note/Tips


## Supplement

-  `sampling_callback()` の第1引数 `context`は「その要求がどういう文脈で来たか」というメタ情報とセッションへのハンドルを運ぶ引数
   -  context が要るのは、たとえば長い生成の途中で context.session を通じて進捗を Server に通知したい、request_id でログを紐づけたい、セッションに持たせた共有リソースにアクセスしたい、といったケース。今回のようにメッセージを LLM に流して結果を返すだけなら触らなくて済む、という位置づけ。


## Reference

