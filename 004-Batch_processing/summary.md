# [Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing)

## summary

- **Batch processing** : Batches APIを用いて非同期に処理すること。
  -  標準API価格に対して一律50%コストカットされ、Throughputを増やすことも可能。
  - *有効なケース*
    - 迅速なResponseを要さないとき
    - コストを最適化したいとき
    - 大規模の要求(評価・解析・推論)を処理したいとき
- **Batchs API**
  - 全モデル対応
  - 料金は標準API価格の50%<sup>[1](#ref1)</sup>

- 概要:
  - `client.messages.batches.create()`を使って複数の要求を一度に送信し、
  - そのResponse`message_batch`からバッチに割り当てられたIDを取得し、
  - `client.messages.batches.retrieve(ID).processing_status`により"ended"であるまで繰り返しステータスを確認し、
  - 完了したら、`client.messages.batches.results(ID)` で結果（`.jsonl`）をストリーミングし、1件ずつ処理するという流れ

- 制約
  - 100,000 メッセージ か 256 MBまで
  - 処理は大半が1時間以内。ただしこれは平均であって保証ではないため、blocking判定にもSLA計算にも使ってはならない（※distractorの定番）
  - 結果を待つ主体がいる場合（=blocking workflow）はBatch不可。同期APIを使う
  - 全件完了か24時間経過の早い方で結果取得可能で、24時間を超えたリクエストは expired となる。そのためSLA(Service Level Agreement)が30時間以内とすると最悪時間が24時間であるから、Batch間隔を6時間とすると、Batch投入直後のRequestは次の投入までの待ち時間6時間+最悪実行時間24時間で合わせて30時間かか り、後処理を含めると、SLAを守れない。そのため、Batch間隔を4時間などに狭め、28時間+そのほかの処理時間 < 30を達成する、という設計をしなくてはならない。
  - また SLA < 24h ならバッチ自体が選べない（間隔をどれだけ詰めても24時間の壁は動かない）

## Note/Tips

- 🌟Best practice
  - ステータスが正常に処理されているかを監視し、fail時に適切なretryがなされるように実装すること.
    - 具体的には、failしたbatchのcustom_id で失敗分を特定し、失敗文のみを再投入。コンテキスト長超過だったものはチャンク分割するなど適切な修正を加えるなどの工夫をする必要がある。
  - `custom_id`は意味のある文字列を使うこと（結果は投入順に返らないため、突き合わせは `custom_id` に頼るしかない）
  - 巨大なデータセットは複数のバッチに分けること
  - Validation Errorを避けるために簡単なRequestでDry-Runすること

## supplement

-  🌟1リクエスト内でクライアント側ツールの往復は完結しない（tool_use で止まるため、tool_result を付けて再投入する）。サーバーツールはバッチ側でループが回り、未完時は `pause_turn` が返る

- 結果を取得すると、各リクエストに以下いずれかの `result.type` が付く（バッチ全体の processing_status は in_progress / canceling / ended の3値。 canceling は中間状態で、最終的には必ず ended に落ちる）
  - succeeded: 正常
  - errored: internal server error や 無効なRequestがなされた場合
  - canceled: UserがLLMにBatch処理する前にキャンセルした場合
  - expired: Requestされてから24時間以上経過していた場合

- code例
  ```python
  from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
  from anthropic.types.messages.batch_create_params import Request

  from anthropic import Anthropic

  client = Anthropic()

  message_batch = client.messages.batches.create(
    requests=[
      Request(
        custom_id="xxx",
        params=MessageCreateParamsNonStreaming(
          model="claude-haiku-5",
          max_tokens=100,
          messages=[
            {
              "role": "user",
              "content": "hello"
            }
          ]
        )
      ),
      Request(
        custom_id="xxx2",
        params=MessageCreateParamsNonStreaming(
          model="claude-haiku-5",
          max_tokens=100,
          messages=[
            {
              "role": "user",
              "content": "Hi again"
            }
          ]
        )
      )
    ]
  )

  ## output : message_batch
  # {
  #   "id" : "msgbatch_brahbrah",
  #   "type": "message_batch",
  #   "processing_status": "in_progress",
  #   "request_counts": {
  #     "processing": 2,
  #     ...
  #   },
  #   "created_at": "2026-08-13T...",
  #   ...
  # }

  import time

  MESSAGE_BATCH_ID = message_batch["id"]
  while True:
    res_batch = client.messages.batches.retrieve(MESSAGE_BATCH_ID)
    if res_batch.processing_status == "ended":
      break

    print(f"Batch {MESSAGE_BATCH_ID} is still processing ...")
    time.sleep(60)
  print(res_batch)
  ```

- `message_batch` はSDKのオブジェクトなので `message_batch["id"]` では取り出せず、`message_batch.id` と書く必要があります（出力のJSON表示に引きずられやすい箇所）。

- `errored` / `canceled` / `expired` になったリクエストは課金されない。また、1件の失敗は同じバッチ内の他リクエストの処理に影響しない。
- `custom_id` は 1〜64文字・英数字とハイフン・アンダースコアのみで、バッチ内で一意である必要がある。
- バッチは Workspace 単位でスコープされ、同じ Workspace の API キーからしか参照できない。
- 送信済みのバッチは変更できない。変えたい場合はキャンセルして作り直す（`processing_status` が `canceling` → `ended` となり、キャンセル前に処理済みの分は部分結果として残る）。
- Prompt caching と併用でき割引は積み上がるが、非同期・並行処理のためキャッシュヒットはベストエフォート（実測30〜98%）。バッチは5分を超えることが多いため、1時間キャッシュを使うとヒット率が上がる。
- `stream: true` などバッチでは使えないパラメータがあり、含めると validation error になる。この検証はバッチ処理の終了後にまとめて返るため、Dry-Runの価値が高い。

## reference

<a src="#ref1"></a>

1. [Pricing](https://platform.claude.com/docs/en/build-with-claude/batch-processing#pricing)


