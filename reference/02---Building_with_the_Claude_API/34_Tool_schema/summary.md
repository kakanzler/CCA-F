# [Tool schemas](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287753)

## Summary

- *Tool schema* : 作成したToolをClaudeに伝えるためのJSON schema.
  - Schemaの構造は以下
    ```json
    {
        "name" : "tool名",
        "description" : "何のためのToolか、いつ使うのか、何を返却するか",
        "input_schema" : {
            "type":"object",
            "properties": {
                "引数名": {
                    "type": ,
                    "description": "引数の説明",
                    "default": "default値"
                }
            },
            "required" : []
        },
    }
    ```

## Note/Tips

- Descriptionの効果的な書き方
  1. 3，4文でToolが何をするのか説明する
  2. Toolをいつ使うべきかは詳細に記載する
  3. Toolがどんな種類のOutputをするのかを記載する
  4. それぞれの引数について詳細情報を記載する

- ※ ただし、これもClaudeに書かせてしまってもいい
  - 具体的にはAnthropicのToolUseのページとToolをコピーし、ClaudeにJSON Schema生成を依頼する

- JSON Schemaの定義
  - `anthropic.types.ToolParam`で型定義して書く。（単純にDict型で書いてもいいが、型定義したほうが堅牢）

## Supplement

- JSON Schema自体はAI/tool calling専用の仕様ではなく、以前から広く使われている**汎用のデータ検証仕様**。AI界隈が「関数の引数を記述するのに便利」という理由で流用しているだけ。
- `input_schema` の中身は素のJSON Schema。`type: "object"` / `properties`（各引数の型・説明・default）/ `required`（必須引数名の配列）が基本形。default があり省略可能な引数は `required` を空配列にする。
- 命名規約: 関数 `foo` に対してスキーマは `foo_schema` と命名する。関数とスキーマの対応が一目で分かるようにするため。
- `ToolParam` は機能上必須ではない（Dictのままでも動く）。API呼び出し時の型エラーを事前に検出するためのもの。

## Reference


- [Cluade Platform Docs : Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)

## Memo

- ClaudeにJSON Schemaかかせてみた。
  - *input*
      ```python
      def get_current_datetime(
          date_format="%Y-%m-%d %H:%H:%S"
      ):
          if not date_format:
              raise ValueError("date_format cannot be empty")
          return datetime.now().strftime(date_format)
      ```
      このToolのJSON Schemaを作成して。
      参考: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
  - *output*
      ```json
      {
          "name": "get_current_datetime",
          "description": "Returns the current local date and time of the machine running this tool, formatted as a string. Use this whenever you need to know 'now' — for timestamping, computing relative dates (e.g. 'next Friday'), or answering questions about the current date or time. Do not use it for past or future dates, or for time in other time zones: the result always reflects the host's local system clock with no timezone conversion and no timezone offset in the output. The date_format parameter is a Python strftime format string that controls the output layout only; it does not change which moment is returned. If omitted, the format defaults to '%Y-%m-%d %H:%M:%S' (e.g. '2026-08-04 09:30:00'). Passing an empty string raises an error.",
          "input_schema": {
              "type": "object",
              "properties": {
                  "date_format": {
                      "type": "string",
                      "minLength": 1,
                      "default": "%Y-%m-%d %H:%M:%S",
                      "description": "Python strftime format string, e.g. '%Y-%m-%d' for date only, '%H:%M' for time only, '%Y-%m-%dT%H:%M:%S' for ISO-like output. Omit this parameter unless the user or task requires a specific layout. Must not be empty."
                  }
              },
              "required": [],
              "additionalProperties": false
          },
          "input_examples": [
              {},
              { "date_format": "%Y-%m-%d" },
              { "date_format": "%Y年%m月%d日 %H時%M分" }
          ]
      }
      ```

- Claudeに書かせたJSON SchemaをPythonで定義
    ```python
    from anthropic.types import ToolParam

    get_current_datetime_schema = ToolParam({
        "name": "get_current_datetime",
        "description": "Returns the current local date and time of the machine running this tool, formatted as a string. Use this whenever you need to know 'now' — for timestamping, computing relative dates (e.g. 'next Friday'), or answering questions about the current date or time. Do not use it for past or future dates, or for time in other time zones: the result always reflects the host's local system clock with no timezone conversion and no timezone offset in the output. The date_format parameter is a Python strftime format string that controls the output layout only; it does not change which moment is returned. If omitted, the format defaults to '%Y-%m-%d %H:%M:%S' (e.g. '2026-08-04 09:30:00'). Passing an empty string raises an error.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date_format": {
                    "type": "string",
                    "minLength": 1,
                    "default": "%Y-%m-%d %H:%M:%S",
                    "description": "Python strftime format string, e.g. '%Y-%m-%d' for date only, '%H:%M' for time only, '%Y-%m-%dT%H:%M:%S' for ISO-like output. Omit this parameter unless the user or task requires a specific layout. Must not be empty."
                }
            },
            "required": [],
            "additionalProperties": False
        },
        "input_examples": [
            {},
            { "date_format": "%Y-%m-%d" },
            { "date_format": "%Y年%m月%d日 %H時%M分" }
        ]
    })
    ```