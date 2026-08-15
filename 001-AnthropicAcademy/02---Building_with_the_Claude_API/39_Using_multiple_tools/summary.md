# [Using multiple tools](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287749)

## Summary

- 今回は複数のツールを実装し、具体的に**ツール間に依存のある多段呼び出し**の出力を見るためのセクションだったのでMemoに結果を記載するに留める。

## Note/Tips


## Supplement

- どのツールをどの順で呼ぶかはモデル側が決めるので、実装側は while ループを回すだけでよい。

## Reference

## Memo
- 実装例
    ```python

    import json

    def run_tool(tool_name, tool_input):
        if tool_name == "get_current_datetime":
            return get_current_datetime(**tool_input)
        elif tool_name == "add_duration_to_datetime":
            return add_duration_to_datetime(**tool_input)
        elif tool_name == "set_reminder":
            return set_reminder(**tool_input)
        else:
            raise ValueError("Invalid Tool name.")

    def run_tools(message):
        tool_requests = [
            block for block in message.content if block.type == "tool_use"
        ]
        tool_result_blocks = []

        for tool_request in tool_requests:
            try:
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
        while True:
            response = chat(messages, tools=[
                get_current_datetime_schema,
                add_duration_to_datetime_schema,
                set_reminder_schema
            ])
            add_assistant_message(messages, response)

            if response.stop_reason != "tool_use":
                break

            tool_results = run_tools(response)
            add_user_message(messages, tool_results)

        return messages

    messages = []
    add_user_message(messages, "Set a reminder for my doctors appointment. Its 177 days after Jan 1st, 2050.")

    response = run_conversation(messages)
    ## output : response
    # ----
    # Setting the following reminder for 2050-06-27T00:00:00:
    # Doctor's appointment
    # ----
    # [{'role': 'user',
    #   'content': 'Set a reminder for my doctors appointment. Its 177 days after Jan 1st, 2050.'},
    #  {'role': 'assistant',
    #   'content': [TextBlock(citations=None, text='I need to first calculate the date that is 177 days after Jan 1st, 2050, and then set a reminder for you.', type='text'),
    #    ToolUseBlock(id='toolu_01FaWG6oqhLVPwkgaeWjkwUX', caller=DirectCaller(type='direct'), input={'datetime_str': '2050-01-01', 'duration': 177, 'unit': 'days', 'input_format': '%Y-%m-%d'}, name='add_duration_to_datetime', type='tool_use')]},
    #  {'role': 'user',
    #   'content': [{'type': 'tool_result',
    #     'tool_use_id': 'toolu_01FaWG6oqhLVPwkgaeWjkwUX',
    #     'content': '"Monday, June 27, 2050 12:00:00 AM"',
    #     'is_error': False}]},
    #  {'role': 'assistant',
    #   'content': [TextBlock(citations=None, text="Now I'll set a reminder for your doctor's appointment on June 27, 2050 at midnight:", type='text'),
    #    ToolUseBlock(id='toolu_01EFyVZNP8771zk4CjX5cKtw', caller=DirectCaller(type='direct'), input={'content': "Doctor's appointment", 'timestamp': '2050-06-27T00:00:00'}, name='set_reminder', type='tool_use')]},
    #  {'role': 'user',
    #   'content': [{'type': 'tool_result',
    #     'tool_use_id': 'toolu_01EFyVZNP8771zk4CjX5cKtw',
    #     'content': 'null',
    #     'is_error': False}]},
    #  {'role': 'assistant',
    #   'content': [TextBlock(citations=None, text="Perfect! I've set a reminder for your doctor's appointment on **Monday, June 27, 2050 at 12:00 AM**. You'll receive a notification at that time.", type='text')]}]
    ```