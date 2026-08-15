# [Agents and workflows](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287796)

## Summary

- Workflows と Agents は、1回のリクエストで完結しないタスクを扱うための2つの戦略

  - **Workflows**
    - 事前に決められた処理の流れでClaudeを呼び、特殊な問題に対する処理方法
    - なにをClaudeにさせるべきか事前にわかっている場合やアプリのUXがUserをあるタスク群で制限している場合に有効

      - **evaluator-optimizer pattern**
        - *Workflows* の一つ
        - Producer : 入力を受け取り、Outputを作る役
        - Grader : Outputを評価する役
        - Feedback loop : ProducerのOutputがGraderの閾値以下だった場合にProducerへ返却する流れ
        - Iteration : GraderがOutputを受け入れるまでFeedback loopを繰り返す
            ```mermaid
            stateDiagram

                input --> Producer
                Producer --> Grader : Submission
                Grader --> Producer : Feedback
                Grader --> Output : Accepted
            ```

  - **Agents**
    - Claudeには目的とToolを与えるが、同問題解決させるかはClaudeが推論する方法
    - どう問題解決すればいいのか、どんな変数を与えればいいか不明なときに有効

## Note/Tips

- この章のキモ：*Workflow*か*Agents*どちらを使うかの判断はその作業に必要な処理を**どれだけ理解しているか**にある。

- この章ではCAD生成のタスクから**Evaluator-Optimizer**のパターンを見つけたが、このように様々なWorkflowを洗い出すこと自体は目的ではない。将来的に何度も使えるような実装パターンを得ること。

## Supplement

## Reference

