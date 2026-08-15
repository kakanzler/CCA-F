# [Workflows vs agents](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287794)

## Summary

- まとめ
    ||Workflow|Agents|
    |---|---|---|
    |when to use?| You know how to break down the task and flows| You don't know flow or what task should solve |
    |how to use? |predefine each steps to solve the portion of problem broken down |give tools and goals|
    | Accuracy | ◎ | 〇 (depending on Claude) |
    | easy to test | ◎ | △~× (it's hard to instrument, test, evaluate) |
    | Flexibility | △~× (rigid flow) | ◎ |
    | UX | △ (need correct input) | ◎ |
    | Reliability | ◎ | 〇 |


## Note/Tips

- 基本的にはWorkflowが優先される。信頼性、予測可能性を担保できるから。現実的に事前にフローを決めるなどが難しい場合にAgentsを利用する。

## Supplement

- Workflow の精度が高いのは「分割」そのものが理由。大ききなタスクを小さなサブタスクに割り、1回の呼び出しで Claude が扱う範囲を狭めるほど精度が上がる。逆に Agents は、設計時に想定していなかったツールの組み合わせを Claude 自身が作れるため、未知のタスクに対応できる。この一点が両者の長所と短所を同時に説明している。

- Agents 固有の性質として、必要に応じて Claude 側からユーザーに追加入力を求められる（フローが固定されていないため対話的に補える）。

## Reference

