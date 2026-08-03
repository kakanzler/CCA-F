# [Response Streaming](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287734)

## Summary

- **Response Streaming** : 生成が終わるまでの間、Userに生成途中のChunkを少しずつ見せ、UXを向上させるためのUI上への出力方法。

- streamの大まかな流れ
1. Server(API送付側)からClaudeにmessagesを送付(`Anthropic.anthropic.client.messages.create()`)
2. ClaudeはInitial ResponseをServerに返却
3. Claude内でevent毎に,その部分的なOutputをServerへ返却する

- eventは以下の6種類。
  1. *MessageStart*: 新規のメッセージが開始するタイミング
  2. *ContentBlockStart*: 新規のBlockが開始されるタイミング
  3. *ContentBlockDelta*: 生成されたOutputの１チャンクそのものの出力タイミング(イベントに1チャンクも入っている)
  4. *ConetnBlockStop*: 現在生成中のBlockが終わったことを告げるタイミング
  5. *MessageDelta*: 現在のメッセージの完成タイミング
  6. *MessageStop*: 現在のメッセージの終了タイミング

- Streamの確認の方法
1. `Anthropic.anthropic.client.messages.create()`の引数に`stream=True`を追加することでstreamとして受け取る。
2. それをfor文でIterateして確認可能。

- 実際のStreamの確認方法
1. `client.messages.stream()` を with 文（context manager）で使う。`stream=True` は不要。
2. `stream.text_stream` をiterateすると、テキスト以外のイベントを自動で除外し、表示に必要な本文チャンクだけを逐次取得できる（生イベントを手動でパースする必要がない）。
3. 最終的な出力は`stream.get_final_message()`で得る。

### Note/Tips


## Supplement

- 一連のeventはすべて Claude への「1回のリクエスト」の中で返ってくる。eventごとにAPIを呼び直しているわけではない。
- `ContentBlockStart` のBlockには text だけでなく tool use など他の種類のcontentも入りうる。
- `stream.get_final_message()` の用途は「DB保存や後続処理のために、組み立て済みの完全なメッセージを得る」こと。逐次チャンクはUX用、完全メッセージはアプリケーションロジック用、と役割が分かれる。
- 表記の細かい点: 実際の呼び出しは `client.messages.create()` / `client.messages.stream()`。`Anthropic.anthropic.client...` という属性パスは存在しない（`Anthropic` はクライアントを生成するクラス）。

## Reference

## Memo
- 実装例
    ```Python
    messages = []
    add_user_message(
        messages=messages,
        text="Claude Certified Architect – Professional についてCCA_F,CCAR_Fなどとの違いを1sentenceで教えて"
    )
    stream = client.messages.create(
        model=model,
        max_tokens=100,
        messages=messages,
        stream=True
    )

    for event in stream:
        print(event)

    ## output : print
    # RawMessageStartEvent(message=Message(id='msg_011CdfqdLC5SZScLmhyTH8oi', container=None, content=[], model='claude-haiku-4-5-20251001', role='assistant', stop_details=None, stop_reason=None, stop_sequence=None, type='message', usage=Usage(cache_creation=CacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=0, inference_geo='not_available', input_tokens=41, output_tokens=1, output_tokens_details=None, server_tool_use=None, service_tier='standard')), type='message_start')
    # RawContentBlockStartEvent(content_block=TextBlock(citations=None, text='', type='text'), index=0, type='content_block_start')
    # RawContentBlockDeltaEvent(delta=TextDelta(text='#', type='text_delta'), index=0, type='content_block_delta')
    # RawContentBlockDeltaEvent(delta=TextDelta(text=' Claude認定資格の違い\n\nClaude Certified Architect – Professional (CCA-P)', type='text_delta'), index=0, type='content_block_delta')
    # RawContentBlockDeltaEvent(delta=TextDelta(text='は、Claude APIの実装に関する最上位の認定資格であ', type='text_delta'), index=0, type='content_block_delta')
    # RawContentBlockDeltaEvent(delta=TextDelta(text='り、CCA_FやCCAR_Fなどの基礎レベル', type='text_delta'), index=0, type='content_block_delta')
    # RawContentBlockDeltaEvent(delta=TextDelta(text='資格よりも、より複雑なシステム設計や本番', type='text_delta'), index=0, type='content_block_delta')
    # RawContentBlockDeltaEvent(delta=TextDelta(text='環境での実装能力が求められます。', type='text_delta'), index=0, type='content_block_delta')
    # RawContentBlockStopEvent(index=0, type='content_block_stop')
    # RawMessageDeltaEvent(delta=Delta(container=None, stop_details=None, stop_reason='end_turn', stop_sequence=None), type='message_delta', usage=MessageDeltaUsage(cache_creation_input_tokens=0, cache_read_input_tokens=0, input_tokens=41, output_tokens=98, output_tokens_details=None, server_tool_use=None))
    # RawMessageStopEvent(type='message_stop')

    with client.messages.stream(
        model=model,
        max_tokens=1000,
        messages=messages
    ) as stream:
        for text in stream.text_stream:
            print(text, end="")

        final_message = stream.get_final_message()

    # Claude Certified Architect – Professional の位置づけ

    ## output : print
    # Claude Certified Architect – Professional は、**Anthropic社によるClaudeの認定資格体系における最高レベルの認定資格**で、CCA_F（Foundation）やCCAR_F（Associate Foundation）などの初級・中級資格よりも、Claudeの高度な機能・プロンプトエンジニアリング・エンタープライズ導入に関する実践的な知識と技能を要求する上級資格です。

    ## output : final_message
    # ParsedMessage(id='msg_011Cdfqsuo3rGe9s7k21zDfG', container=None, content=[ParsedTextBlock(citations=None, text='# Claude Certified Architect – Professional の位置づけ\n\nClaude Certified Architect – Professional は、**Anthropic社によるClaudeの認定資格体系における最高レベルの認定資格**で、CCA_F（Foundation）やCCAR_F（Associate Foundation）などの初級・中級資格よりも、Claudeの高度な機能・プロンプトエンジニアリング・エンタープライズ導入に関する実践的な知識と技能を要求する上級資格です。', type='text', parsed_output=None)], model='claude-haiku-4-5-20251001', role='assistant', stop_details=None, stop_reason='end_turn', stop_sequence=None, type='message', usage=Usage(cache_creation=CacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=0, inference_geo='not_available', input_tokens=41, output_tokens=142, output_tokens_details=None, server_tool_use=None, service_tier='standard'))

    ## output : final_message.content[0].text
    # '# Claude Certified Architect – Professional の位置づけ\n\nClaude Certified Architect – Professional は、**Anthropic社によるClaudeの認定資格体系における最高レベルの認定資格**で、CCA_F（Foundation）やCCAR_F（Associate Foundation）などの初級・中級資格よりも、Claudeの高度な機能・プロンプトエンジニアリング・エンタープライズ導入に関する実践的な知識と技能を要求する上級資格です。'

    ```