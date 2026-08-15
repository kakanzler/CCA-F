# [Accessing the API](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287726)

## Summary

- ClaudeのAPIの流れ: 5 Steps
    ```mermaid
    sequenceDiagram
    autonumber

        UI ->> Server : request
        Server -) AnthropicAPI : request
        AnthropicAPI ->> AnthropicAPI : model processing
        AnthropicAPI --) Server: response
        Server -->> UI : response
    ```
  - API要求時必要な引数は以下
    - *API Key*: 認証に必要
    - *Model*: LLMの指定に必要
    - *Messages*: Promptが必要
    - *Max Tokens*: LLM処理にあたってClaudeが生成可能なTokenの制限。

- Claudeにおける処理の流れ
  1. Tokenization
     - inputとなるテキスト情報(Prompt)をtoken(より細かい単位、チャンク)に分割
  2. Embedding
     - それぞれのTokenをベクトル化する。この時点のベクトルはその単語が持ちうる全ての意味（例: "quantum" なら物理量の単位・量子力学・極小・量子計算）を併せ持った「数値化された定義」であり、まだ文脈による絞り込みは行われていない。
  3. Contextualization
     - ClaudeはEmbeddingしたそれぞれの値からそのInput上のContextを踏まえたうえでの意味を決定する。
  4. Generation
     - ContextualizedしたEmbeddingベクトルを出力層に通し、次に来る語ごとの確率を計算して1語を選ぶ。Claudeは必ずしも最も高い確率の語を選ぶわけではなく、制御されたランダム性を加えることで自然で多様性に富む出力を実現する。選んだ語は系列の末尾に追加され、その系列を入力として同じ処理を繰り返す（自己回帰）。

- Claudeは以下の場合、推論を止める。
  - *Max tokens reached*: トークン数が上限に達したとき
  - *Natural ending*: **end-of-sequence tokne**が生成された時(通常これで終わる。)
  - *Stop Sequence*: 事前に定義された*Stop phrase*にこの過程の中で見つかったとき

- 推論が完了したら、APIは以下をResponseとして返却する。
  - Message : 生成されたメインとなるOutput(Anthoropic APIから取得したOutputをServerからUserのUIに返却するもの)
  - Usage : 消費したTokenの数。InputとOutputで別々にカウントされて返る。
  - Stop reason : 上記3つのうちどれで終わったのか。

### Note/Tips

- サービスを作るうえでの心がけ
  - API Keyはサーバ側にのみ保持する（→ Supplement 参照）
  - 5 Stepsのどの段階で問題が起きうるかを把握しておくとDebugが早い

## Supplement

- ClientからいきなりAnthropicAPIに投げないのは以下のSecurity要件のためだ。
  - APIが認証のためにAPI Keyを要すること
  - ClientにこのKeyを保持して通信する場合、Keyをネットワーク上に公開することになりSecurity上の脆弱性につながる(誰でもKeyを盗み取り、それだけでなくその通信を不正な要求に変更できてしまう)

- *Messages* は単一の文字列ではなく**リスト**である。今回は「userの入力1件」だけだが、この形式のおかげで会話履歴を積み上げて渡せる。

## Reference

