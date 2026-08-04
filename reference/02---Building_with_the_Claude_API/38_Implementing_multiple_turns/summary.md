# [Implementing multiple turns](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287758)

## Summary

- Claudeからのtoolの要求をどう呼び出すか、を実装するかについてのセクション

- *検知*
  - `stop_reason`が`"tool_use"`だった場合、Claudeからの`tool call`であるのでこれで検知できる。

- *実装*
  1. Loop部
    - 前回のWhile文内でLoopし、検知で記載した"stop_reason"がtool_use"の場合にループするよう設計
  2. Tool呼び出し部
    - if文で呼び出されているtool名前を判定し、適合するToolがあれば、それを呼び出すという設計
  3. エラー処理部
    - 複数のTool要求だった場合、どのToolでエラーが起きたのかは終えるのが望ましい。なので、`run_tools()`でエラーが発見された場合は対応するtool(tool_id)に対しエラー結果をmessage(tool result block)に挿入する。
  4. 複数のツールに対応させる
    - *run_tool()*というヘルパー関数を作成することで、追加で実装する必要が生まれたときにリファクタリングしやすくなる。


## Note/Tips


## Supplement

- 終了条件を `stop_reason != "tool_use"` という**否定形**で書くのが定石。`stop_reason == "end_turn"` を決め打ちにすると、`max_tokens` や `stop_sequence` で停止したケースを拾えず無限ループになる。
- ループ内の**順序**が重要: `add_assistant_message()` は `stop_reason` 判定より**前**に置く。判定の後ろに置くと、break したときの最終回答（assistantメッセージ）が履歴に残らない。
- 「4. 複数のツールに対応させる」は *ツールの種類* を増やす話（名前 → 実装のルーティング）。これとは別に、**1回のレスポンスに複数の `tool_use` ブロックが同時に含まれる**ケースがあり、`run_tools()` 冒頭の内包表記 `[block for block in message.content if block.type == "tool_use"]` はそちらへの対応。lesson 36 の「tool_result は1つの user メッセージにまとめて返す」と対になる。
- エラー処理の理由を「どのToolで失敗したか追える」と書いているが、より本質的な理由は **失敗しても tool_result を必ず返さないと tool_use との対応が崩れてリクエスト自体が通らない**こと（lesson 36 既出）。`try/except` を `for tool_request in tool_requests` の**内側**に置くのもこのためで、1つ失敗しても残りのToolの結果は正常に返せる。
- `run_tool()` の `else` で `raise ValueError` しているのは、`run_tools()` 側の `try/except` に拾わせて `is_error: True` の tool_result に変換させる設計。未知のtool名が来ても会話ループが落ちない。

## Reference

## Memo

- 実装例
    ```python
    import json

    # 4. 複数のツールに対応させる
    def run_tool(tool_name, tool_input):
        if tool_name == "get_current_datetime":
            return get_current_datetime(**tool_input)
        else:
            raise ValueError("Invalid Tool name.")

    def run_tools(message):
        tool_requests = [
            block for block in message.content if block.type == "tool_use"
        ]
        tool_result_blocks = []

        for tool_request in tool_requests:
            # 3. エラー処理部
            try:
                # 2. Tool呼び出し部
                tool_output = run_tool(tool_request.name, tool_request.input)
                tool_result_block = {
                    "type" : "tool_result",
                    "tool_use_id" : tool_request.id,
                    "content" : json.dumps(tool_output),
                    "is_error" : False
                }
            except Exception as e:
                tool_result_block = {
                    "type" : "tool_result",
                    "tool_use_id" : tool_request.id,
                    "content" : f"Error: {e}",
                    "is_error" : True
                }
            tool_result_blocks.append(tool_result_block)

        return tool_result_blocks


    def run_conversation(messages):
        # 1. Loop部
        while True:
            response = chat(messages, tools=[get_current_datetime_schema])
            add_assistant_message(messages, response)

            if response.stop_reason != "tool_use":
                break

            tool_results = run_tools(response)
            add_user_message(messages, tool_results)

        return messages

    # 実行部
    messages = []
    add_user_message(messages, "現在の時刻に3時間足した時刻を教えて")

    response = run_conversation(messages)
    response

    ## output : ressponse
    # [{'role': 'user', 'content': '現在の時刻に3時間足した時刻を教えて'},
    #  {'role': 'assistant',
    #   'content': [TextBlock(citations=None, text='現在の時刻を確認してから、3時間足した時刻を計算します。', type='text'),
    #    ToolUseBlock(id='toolu_01SqL2QFWyrjQ65awuDYqdGr', caller=DirectCaller(type='direct'), input={}, name='get_current_datetime', type='tool_use')]},
    #  {'role': 'user',
    #   'content': [{'type': 'tool_result',
    #     'tool_use_id': 'toolu_01SqL2QFWyrjQ65awuDYqdGr',
    #     'content': '"2026-08-04 22:35:53"',
    #     'is_error': False}]},
    #  {'role': 'assistant',
    #   'content': [TextBlock(citations=None, text='現在の時刻は **2026年8月4日 22:35:53** です。\n\n3時間足すと **2026年8月5日 01:35:53** になります。', type='text')]}]
    ```