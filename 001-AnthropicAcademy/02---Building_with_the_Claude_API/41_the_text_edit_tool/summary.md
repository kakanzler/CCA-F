# [The text edit tool](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287760)

## Summary

- **text edit tool** : Claude標準搭載のbuilt-in tool.
  - できること: ファイル/ディレクトリの閲覧・文字列置換・新規作成・行挿入、および直前の編集の取り消し（undo）

- *実装方法*
  - 通常の tool は『スキーマ + 実装』の両方を自分で書くが、text edit tool は**スキーマだけが Claude に内蔵されている**。リクエスト時に model に応じた小さなスキーマスタブを渡せば、Claude が裏で完全なスキーマに展開してくれる。ただし**ファイル操作の実装は依然として自分で書く必要がある**
        ```python
        def get_text_edit_schema(model):
            if model.startswith("claude-3-7-sonnet"):
                return {
                    "type": "text_editor_20250124",
                    "name": "str_replace_editor",
                }
            elif model.startswith("claude-3-5-sonnet"):
                return {
                    "type": "text_editor_20241022",
                    "name": "str_replace_editor",
                }
        ```



## Note/Tips


## Supplement

- なぜ`text edit tool`がビルトインかというと、作業環境の理由によりEditorが使えなかったり、統合時、直接Claudeにはファイル操作などで着てほしいなどの理由があるから。

- Claude4以降は"text_editor_20250728"であると記載がある。<sup>[1](#ref1)</sup>

> - 位置づけとしては「AI コードエディタの機能を、自前のアプリケーションの中に再現するための部品」。エディタが既にあるなら不要で、**プログラムからファイル編集させたいとき**に効いてくる。


## Reference

<a src="#ref1"></a>

1. [Text editor tool : mplement the text editor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool#implement-the-text-editor-tool)
    ```
    The tool type is type: "text_editor_20250728" for Claude 4 and later models.
    ```