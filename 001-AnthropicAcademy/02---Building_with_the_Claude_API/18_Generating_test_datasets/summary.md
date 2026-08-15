# [Generating test datasets](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287739)

## Summary

- PromptのPlaceholderに結合できるようにDatasetをJSONのリストで作成する
    ```json
    [
        {
            "placeholder": "Create ~~~"
        },
        {
            "placeholder": "Create ~~~"
        },
        ...
    ]
    ```
- 作成にはClaudeを使えばよく。以下のようにpromptを作成しclaudeにRequestすればよい。
    ```python
    def generate():
        prompt = """
    Generate an evaluation dataset for ~~~.

    Example output:
        ```json
        [
            {
                "placeholder": "brah brah brah"
            },
            {
            ...
            },
            ...
        ]
        ```

    * Focus on tasks that ~~~

    Please generate N objects.

    """
    ```
- その後は assistant_messageに`{"```json"}`をいれて、`client.message.create(stop_sequences=["```"])`とすることでjson部分を出力させ、`json.dump()`で保存するという流れ。

## Note/Tips

- データセット生成は「評価対象のプロンプトを動かすモデル」と同じモデルである必要はない。テストデータ作成は補助タスクなので Haiku のような高速・低コストのモデルで十分であり、評価本体（Claude へのフィード）とは切り離してモデルを選んでよい。

## Supplement


## Reference
