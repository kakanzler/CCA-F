# [Multi-Turn Conversation](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287735)

## Summary

- Claudeは自身で会話履歴をどこにも保持しない。RequestはあくまでStatelessなもので個別のもの。
- 会話のやりとりを維持するためにやることは2つ。
  1. 手動でメッセージ履歴をコードで保持すること
  2. 毎回のRequestでそれまでの完全な会話履歴をすべて送信すること

- 流れ
  1. "user"でメッセージをClaudeに送信する
  2. Cluadeからメッセージを受領し、"assistant"でメッセージリストに自分で追加する
  3. "user"で追加のメッセージをメッセージリストに加える
  4. メッセージリストをまるごとClaudeに送信する

### Note/Tips


## Supplement

- 履歴を送らない場合の具体的な症状: 「量子コンピュータとは?」の次に「もう一文書いて」と送ると、Claudeは全く無関係な話題の一文を返す。これは「忘れた」のではなく、そもそも前のやりとりを一度も受け取っていないため。
- `messages` リストそのものが会話状態のすべてであり、API側には何も残らない。したがって assistant の応答を自分で追加し忘れると、その turn は会話からまるごと消える。
- 毎回すべての履歴を送り直す構造上、会話が伸びるほど入力トークンが増え続ける（コスト・レイテンシに直結する）。

## Reference

## Memo
- 具体的な実装
  - ヘルパー関数を設計する
    ```python
    from typing import Optional


    def add_user_message(
        messages : list[Optional[dict[str, str]]],
        text: str
    ):
        user_message = {
            "role" : "user",
            "content" : text
        }
        messages.append(user_message)

    def add_assistant_message(
        messages: list[Optional[dict[str, str]]],
        text: str
    ):
        assistant_message = {
            "role" : "assistant",
            "content" : text
        }
        messages.append(assistant_message)

    def chat(
        messages: list[Optional[dict[str, str]]]
    ):
        message = client.messages.create(
            model=model,
            max_tokens=100,
            messages=messages
        )
        return message.content[0].text
    ```
  - *流れ*に記載したとおりに実装する
    ```python
    messages = []

    #   1. "user"でメッセージをClaudeに送信する
    add_user_message(
        messages=messages,
        text="忘れないための勉強方法は? in one sentence."
    )
    llm_response = chat(messages)

    # output : llm_response
    # '# 記憶定着の勉強方法\n\n**定期的な復習（特に1日後、1週間後、1ヶ月後）と、学んだ内容を実際に使う・教えるなどのアウトプットを組み合わせることが最も効果的です。**'<br>

    #   2. Cluadeからメッセージを受領し、"assistant"でメッセージリストに自分で追加する
    add_assistant_message(
        messages=messages,
        text=llm_response
    )

    #   3. "user"で追加のメッセージをメッセージリストに加える
    add_user_message(
        messages=messages,
        text="エビングワースの忘却曲線はどう？ in one sentence."
    )

    #   4. メッセージリストをまるごとClaudeに送信する
    llm_response2 = chat(
        messages=messages
    )

    # output : llm_response2
    # '# エビングワースの忘却曲線について\n\n**忘却曲線は時間とともに記憶が急速に低下することを示しており、この理論に基づいて復習のタイミングを計画する「間隔反復学習」が効果的な勉強法として広く活用されています。**'
    ```