# [Making a request](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287725)

## Summary

- `dotenv.load_dotenv()`により、作業ディレクトリにある.envを読むことが可能。これにより`.env`ファイルにAPI_KEYを環境変数として配置し、セキュアにNotebookなどのコード内で読み取ることが可能。

- `anthropic.Anthropic()`は`api_key`未指定時に環境変数`ANTHROPIC_API_KEY`を読むため、`client = Anthropic()`だけでよい。

- LLMへのリクエストは以下を引数で指定する。
  - *model* : `claude-haiku-4-5`などのaliasを用いてモデルを選択する。
  - *max_tokens* : セーフティ。モデルが勝手にTokenを消費しすぎないように設定する。
  - *messages* : `{"role" : "user", "content" : "hello"}`のようなdict型を要素とするlistを引数にする。
    - Messageは2種類ある。
      - *User message*
        - Userから送信されるメッセージ。(Prompt)
        - `"role" : "user"`で指定する。
      - *Assistant message*
        - Userのメッセージに対しLLMが推論した結果。つまり返却されるメッセージ。
        - `"role" : "assistant"`で指定する。
- 戻り値の`Message`オブジェクトはメタデータを含み、生成テキストは`content`（ブロックのlist）の要素として入っている。テキストだけ欲しい場合は`message.content[0].text`で取り出す。

### Note/Tips

- messagesには複数のメッセージを送信できるため、*userのメッセージ＋それに対するLLMの出力+それに対するUserのメッセージ*のような流れをmessageとして送信できる。そのためにroleを指定できるようになっている。

## Supplement

- API_KEYは秘匿情報なので、構成管理対象からは除外すること(`.gitignore`)。
- Notebookで`print(os.getenv("API_KEY"))`などとしてしまうとloacl_historyに実行結果が残ってしまうので絶対に出力してはならない。(コードブロックを消しても無意味)
- もし、printしてしまったら、KeyをRotationすることを推奨。
- `max_tokens`は上限であって目標値ではない。モデルはこの値に到達しようとはせず、適切と判断した長さで書いて終わる。上限に当たった場合は要約されるのではなく**途中で打ち切られる**（`stop_reason`が`end_turn`ではなく`max_tokens`になる）。


## Reference

- [Anthropic: Claude Platform Docs: Python SDK](https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python)


## Memo

- 実行結果

```python
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5"

message = client.messages.create(
    model=model,
    max_tokens=100,
    messages=[
        {
            "role" : "user",
            "content": "say hello there!"
        }
    ]
)


print(message.content[0].text)

### output
# > 'Hello there! 👋'

print(message)

### output
# > Message(id='msg_011CddaFu1ur6woSBcXq4byA', container=None, content=[TextBlock(citations=None, text='Hello there! 👋', type='text')], model='claude-haiku-4-5-20251001', role='assistant', stop_details=None, stop_reason='end_turn', stop_sequence=None, type='message', usage=Usage(cache_creation=CacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=0, inference_geo='not_available', input_tokens=11, output_tokens=9, output_tokens_details=None, server_tool_use=None, service_tier='standard'))
```
