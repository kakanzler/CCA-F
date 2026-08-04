# [Fine grained tool calling](https://anthropic.skilljar.com/claude-with-the-anthropic-api/313160)

## Summary

- **Response Streaming**をClaudeからの`tool use`に適応する場合、Event: `InputJsonEvent`を処理する必要がある。
  - `InputJsonEvent` ("stream[].type = "input.json")
    - この時取り出せる情報は以下の二つ。用途に応じて使いたい方を選ぶ。
      1. *partial_json* : Toolの引数のJSON形式の一部分
         - ex. {'title': 'HarryPotter'} なら、{'title, ':, 'Harry, Potter'}
      2. *snapshot* : これまでに受け取ったJSONが累積し生成された一つのJSON
         - ex. {'title ->  {'title': -> {'title':'Harry -> {'title':'HarryPotter'}
- `chunk`の処理方法
  - default : Anthropic APIはすぐにはすべてのChunkを送信しない。top-levelのkey-valueのペアが完成したら、Validateして、問題なければそれぞれのChunkを送る設計。
    - 例: `{"aaa": "...", "bbb": {...}}` を返すToolなら、まず `aaa` の値が揃った時点でValidateして `aaa` 分のChunkをまとめて送信し、次に `bbb` オブジェクト全体について同じことを行う
  - **Fine-Grained Tool Calling**: Claudeが生成したChunkを逐一ほしい場合に有効化する。
    - `client.beta.messages.stream(..., betas=["fine-grained-tool-streaming-2025-05-14"])`とすることで有効化される。
    - この時`word_count`がすぐ返却されるようになる。
    - JSON Validationは事前に使用されない為、自前でValidateする必要がある。
      - `json.loads()` して `json.JSONDecodeError` なら次のchunkを待つ、という実装自体は簡単。ただしfine-grainedではAPI側の補正が効かないため、`undefined` のように最後まで不正なままの値が来る可能性があり、最終的なJSONの妥当性は自分で担保する必要がある

## Note/Tips

- **Fine-Grained Tool Calling**は以下の場合に有効。
  - できるだけ早く更新状況を伝える必要がある場合
  - BufferによるDelayが発生しUXが下がることを嫌う場合
  - 堅牢なJSONエラーハンドリングを自前で実装する覚悟がある場合（＝これが前提条件）

## Supplement

- 既定はValidationあり: 原文は「大半のアプリケーションでは既定の挙動で十分」と明言している。fine-grainedは常用するものではなく、Bufferの遅延がUXを実際に損なっている時に限って開ける逃げ道、という位置づけ。

- APIの仕様の「溜めてから一気に送る」挙動こそが、streamingを有効にしているにもかかわらず、遅延(変化なしの待ち時間)→バースト(一気に送られてくる) と見える理由。

## Reference

