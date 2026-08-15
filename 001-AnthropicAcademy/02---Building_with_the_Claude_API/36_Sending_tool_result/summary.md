# [Sending tool results](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287752)

## Summary

- Claudeからの*Tool use*要求に応じてServer側で実行し、その結果をClaudeに渡す方法についてのセクション

- Claudeには以下のように`"role": "user"`のMessageを含め、`Tool result block`て返却する。
  - *type* : "tool_result"固定
  - *tool_use_id* : Claudeから受領したResponseの*ToolUse block*に入っているトラッキング用のID
  - *content* : Toolの結果。string、または content block のリスト（text / image など）を渡せる
  - *is_error* : エラーが発生している場合、*True*を記載する

- 返却時にも引数`tools=[...]`にtoolのschemaを指定する

## Note/Tips

- Claudeから受領したresponseから情報を取りだしてTool callする際は以下のように、dictをunpack sytanxしてToolに渡す。
    ```python
    tool_result = get_current_datetime(**response.content[0].input)
    ```

## Supplement

- tool_use_idがUniqueなので、複数のTool callがあっても、それぞれのidをClaudeへの返却に紐づけて返すので、Claudeも識別できる
- この帰結として、tool_resultを返す順序はToolUse blockの順序と一致していなくてよい。idで対応づくため、Server側で先に終わったものから詰めて返せる。
- なお `content` を「string」と書いたのはorigin通りで誤りではない（origin: "Output from running your tool, serialized as a string"）。上の本文に追記した「content blockのリストも渡せる」はAPI仕様としての補足。

- 複数のTool callを返す場合、tool_resultブロックは「1つのuserメッセージにまとめて」入れる必要がある。分割して複数メッセージで返すと、Claudeが並列Tool callをしなくなる方向に学習してしまう。

- is_error を立てた失敗結果も省略せず返す。返さないと tool_use と tool_result の対応が崩れる。
- tools=[...] を返却時にも渡すのは、APIがステートレスで毎回リクエスト全体を組み立て直すため。tool schema を落とすとClaudeは受け取ったtool_resultが何のToolのものか解釈できない。
- Note/TipsとReferenceで `response.content[0]` を使っているが、originは `response.content[1]`（TextBlockが0、ToolUseBlockが1）。lesson 35で書いた通りindexは保証されないので、実装では type で判別して取り出すこと。

## Reference

  -  実装例
    ```python
    messages.append(
        {
            "role" : "user",
            "content" : [
                {
                    "type": "tool_result",
                    "tool_use_id": response.content[0].id,
                    "content": tool_result,
                    "is_error": False
                }
            ]
        }
    )

    final_resposne = client.messages.create(
        model=model,
        messages=messages,
        max_tokens=100,
        tools=[get_current_datetime_schema]
    )
    ## output : final_response
    # Message(id='msg_011CdhatgYNNCQn76E779uKw', container=None, content=[TextBlock(citations=None, text='The exact time is **19:52:56** (7:52:56 PM).', type='text')], model='claude-haiku-4-5-20251001', role='assistant', stop_details=None, stop_reason='end_turn', stop_sequence=None, type='message', usage=Usage(cache_creation=CacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=0, inference_geo='not_available', input_tokens=1116, output_tokens=23, output_tokens_details=None, server_tool_use=None, service_tier='standard'))
    ```
