# agentic loop(エージェントループ)

## summary

- **agentic loop** : prompt を受け取り、必要に応じてtoolを使用し最終的なAnswerを返すまでの一連の流れのこと。
- Flow
    ```mermaid
    stateDiagram-v2

    Your_Prompt --> Claude_evaluation

    state agentic_loop {
        Claude_evaluation --> Tool_call : tool calls
        Tool_call --> Claude_evaluation : tool result
    }

    Claude_evaluation --> Final_answer : no tool call

    ```
- Agent SDK を使用すると自律的にagentic loopを実装できる
  1.  PromptをSDKがClaudeに送信
  2.  SDKが*SystemMessage*を作成
  3.  agentic loop実施

- ターン数
  - Loop内(Claude_evaluation - Tool_call 間)の1往復+最終メッセージの送信
  - maxTurnで返答までの最大ターン数を制御できるがここでいうTurns数はLoop内のターンのみをさす
  - 実際に確認する場合 ⇒ `ResultMessage.num_turns: int` を見る

- ResultMessageにおける結果確認する際に見るべきフィールド

  - **stop_reason** (str | None)
    - end_turn : モデルの通常終了
    - max_tokens : 出力トークン制限に達した
    - refusal : モデルがリクエストを拒否した
  -  **subtype** (str)
     - *success* : 通常のタスク完了した場合 -> "result"フィールドに結果がstrで出力される。それ以外はNone。
     - *error_max_turns* : max_turns/maxTurns制限に達した場合
     - *error_max_budget_usd* : maxBudgetUsd制限に達した場合
     - *error_during_execution* : API障害などによりLoopが中断された場合
     - *error_max_structured_output_retries* : retry回数内で有効な出力が生成されなかった場合など

  - **is_error** — subtype が "success" でも is_error=True になるケースがあるため、確認するのが安全
  - **terminal_reason** : なぜループが終わったかを示すフィールド。subtype より細かい新しいフィールド。interrupt() による中断を区別できるのが利点。
    - *completed*
    - *max_turns*
    - *aborted_streaming*
    - *aborted_tools*

## note/tips

- Claude API の response.stop_reasonには `tool_use`, `end_turn`が存在する。


## supplement

- API直接実装時のループ制御（← 試験の本命）
  - Claude API の `response.stop_reason` を毎ターン見て分岐する
    - "tool_use"  : tool_use ブロックを実行 → tool_result を messages に追加 → 継続
    - "end_turn"  : ループ終了
  - 上図の「no tool call → Final_answer」が API では stop_reason == "end_turn" に対応
  - SDK はこの分岐を内部で実施しており、SDK利用者が見る stop_reason は
    「ループ終了後の最終ターンの停止理由」なので、"tool_use" は現れない

## reference

- [エージェントループの仕組み](https://code.claude.com/docs/ja/agent-sdk/agent-loop)

- [ResultMeesage (Python)](https://code.claude.com/docs/ja/agent-sdk/python#resultmessage)