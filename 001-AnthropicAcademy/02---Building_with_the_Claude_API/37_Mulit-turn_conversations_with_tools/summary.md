# [Multi-turn conversation with tools](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287750)

## Summary

- Claudeが複数回にわたってtool実行をserverがわへRequestするケースについてのセクション

- 複数回のTool callの処理
  - `while True` 内でループし続け、ClaudeからTool要求がなくなるまではBreakせず、要求に応じたToolを呼び、再度ClaudeへRequestするという仕組み。
    ```python
    def run_conversation(messages):
        while True:
            response = chat(messages)
            add_assistant_message(messages, response)

            # if response isn't asking for a tool:
                # break

            tool_result_blocks = run_tools(response)
            add_user_message(messages, tool_result_blocks)

        return messages
    ```

## Note/Tips

- `isinstance(message, Message)` によりMessageオブジェクトが渡された場合は `message.content`（ブロックのリスト）を取り出す。これで文字列／ブロックのリスト／Messageオブジェクトのいずれも同じヘルパーで扱えるようになる。
- `chat()` がtextではなくMessageオブジェクトを返す設計に変わったため、text_from_messageで `type == "text"` のブロックのみを連結して取り出す。
    ```python
    def text_from_message(message):
        return "\n".join(
            [block.text for block in message.content if block.type == "text"]
        )
    ```

## Supplement

- 以前の回で作成したヘルパー関数をMulti-turn conversationに対応するためにリファクタリングしている。

## Reference

