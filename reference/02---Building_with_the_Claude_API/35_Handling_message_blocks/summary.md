# [Handling message blocks](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287757)

## Summary

- *tool schema*は`client.messages.create()`の引数`tools`としてclaudeに渡す
- `Multi-Block Messages`: ClaudeにToolを渡した際の返却される`Meesageオブジェクト`
  - contentプロパティには以下の2種類のブロックがリストで入る（TextBlockは省略されることがあり、順序・個数は保証されない。type で判別して取り出す）。
    1. *TextBlock* : Claudeがしようとしている内容
    2. *ToolUseBlock* : toolの利用にあたって必要な情報を記載している
       - id : トラッキング用のID
       - input : toolにわたす引数をDict型で{"引数名": "パラメータ"}
       - name : Claudeが利用したいTool名(関数名)
       - tyoe : `tool_use`固定


- 会話履歴の保持はmessagesに追加することでなされる。Toolにおいても同様で以下のように`Messageオブジェクトのcontent部分`を含める。
    ```py
    messages.append({
        "role": "assistant",
        "content": response.content
    })
    ```

- 全体の流れ
    ```mermaid
    sequenceDiagram
    autonumber
    participant a as Server
    participant b as Claude

        a ->> b : message
        b -->> a : Messages
        a ->> a : extract Messages to get tool information Claude need
        a ->> a : tool call
        a ->> a : add `tool result` to messages
        a ->> b : reuest w/ result of Tool
        b -->> a : final response for message

    ```

## Note/Tips



## Supplement

- 会話履歴を残す際、メンテナンス時にトラッキングしたり、人間が読みやすい形のText情報を含めたりするためContentブロックを丸ごと渡す。
- Toolの実行結果を返す際はその`結果`と受け取ったときの`トラッキング用のID`を`"tool_type": "tool_result"`とセットにして`"role": "user"`でmessagesに入れて返す必要がある。

- これまで使ってきた `add_user_message()` / `add_assistant_message()` のようなヘルパー関数は、テキスト文字列だけを想定した実装になっているため、Contentブロックのリストもそのまま受け取れるよう更新が必要になる。


## Reference

- 実装例
```python
# 1, 2
response = client.messages.create(
    model=model,
    max_tokens=100,
    messages=messages,
    tools=[get_current_datetime_schema]
)
## output : response
# Message(
#     id='msg_011CdgyAijq4dbBfG4d3uoca',
#     container=None,
#     content=[
#         ToolUseBlock(
#             id='toolu_01L1JbjKVd7dgjBXgHkkv2Pi',
#             caller=DirectCaller(type='direct'),
#             input={'date_format': '%H:%M:%S'},
#             name='get_current_datetime',
#             type='tool_use'
#         )
#     ],
#     model='claude-haiku-4-5-20251001',
#     role='assistant',
#     stop_details=None,
#     stop_reason='tool_use',
#     stop_sequence=None,
#     type='message',
#     usage=Usage(
#         cache_creation=CacheCreation(
#             ephemeral_1h_input_tokens=0,
#             ephemeral_5m_input_tokens=0
#         ),
#         cache_creation_input_tokens=0,
#         cache_read_input_tokens=0,
#         inference_geo='not_available',
#         input_tokens=1036,
#         output_tokens=63,
#         output_tokens_details=None,
#         server_tool_use=None,
#         service_tier='standard'
#     )
# )

# 3
messages.append({"role": "assistant", "content": response.content})
# 4
tool_result = get_current_datetime(input)
# 5
messages.append({
    "role": "user",
    "content": [
        {
            "type": "tool_result",
            "tool_use_id": response.content[0].id,
            "content": tool_result,
        }
    ]})

# 6, 7
final_response = client.messages.create(
    model=model,
    max_tokens=100,
    messages=messages,
    tools=[get_current_datetime_schema]
)
## output:  final_response
# Message(id='msg_011Cdh2AvDVTpyP5vCsfydeg', container=None, content=[TextBlock(citations=None, text='The exact time is **12:45:33**.', type='text')], model='claude-haiku-4-5-20251001', role='assistant', stop_details=None, stop_reason='end_turn', stop_sequence=None, type='message', usage=Usage(cache_creation=CacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=0, inference_geo='not_available', input_tokens=1116, output_tokens=14, output_tokens_details=None, server_tool_use=None, service_tier='standard'))
```