# [System prompts](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287733)

## Summary

- **Systen Pronpt**
  - `anthropic.client.messages.create()` の引数 `system` に役割や応答方針を渡すことで、会話全体を通して Claude に**どう応答するか**（役割・口調・進め方）を指定し、その役割として振る舞わせ、タスクから逸れないようにできる。
  - ただし、 `system=None`と引数を指定しているのに何も情報を与えない(=None)だとAPIはエラーとなるので注意。

### Note/Tips


## Supplement

- `system` は `messages` の 1 ターンとして積むのではなく `create()` のトップレベル引数として渡す。そのため会話が何ターン続いても指示が効き続ける。

- 同じ質問でも system prompt の有無で答えの形が変わる（例: 数学の家庭教師役を与えると、解答をそのまま出さずヒントと問いかけで誘導する形に変わる）。system prompt が効いているかは「内容が正しいか」ではなく「応答の形が変わったか」で確認するとよい。


## Reference

## Memo

  - 実装結果
    ```python
    def chat(
        messages: list[Optional[dict[str, str]]],
        system: Optional[str] = None
    ):
        params = {
            "model":model,
            "max_tokens":100,
            "messages":messages
        }

        if system:
            params["system"] = system

        message = client.messages.create(**params)

        return message.content[0].text

    answer1 = chat(messages)
    # output : answer1
    # '# エビングワースの忘却曲線について\n\n**忘却曲線は、復習のタイミング（1日後、1週間後、1ヶ月後など）を科学的に示しており、その時点での復習が記憶定着を劇的に高めるため、効率的な学習計画の基礎として非常に有用です'

    system = """
    あなたは英語教師です。英語の勉強について具体的な手順を示す必要があります。
    """

    answer2 = chat(messages=messages, system=system)
    # output : answer2
    # '# エビングワースの忘却曲線について\n\n**学習後1日目、1週間後、1ヶ月後に復習することで記憶の定着率が大きく向上するという科学的根拠があり、英語学習では特に単語や文法を繰り返し復習する際の最適なタイミングを示してくれます'
    ```