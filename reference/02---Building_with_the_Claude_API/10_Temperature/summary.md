# [Temperature](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287728)

## Summary

- **Temperature**
  - Claudeの解答にどれだけ*Predictable*(予測可能性)、*Creativity*(創造性)を持たせるかを示すパラメータ。
  - [0, 1]の閉区間の値で設定する。
  - *Low Temperature* : 確率分布を尖らせ、最高確率のトークンに確率が集中する（＝決定論的な出力）。
  - *High Temperature* : 確率分布を平坦にならし、低確率のトークンも選ばれうる（≒creativeな出力）。

- LLM内部での推論のプロセス
  1. *Tokenization*: Promptをチャンクごとに分割し、ベクトルにする。
  2. *Predication*: ベクトルした値をNNに入力し次に続くトークンの確率を計算する。(ここでは一つに決めず、複数出力される。)
  3. *Sampling*: 2で得た確率からどのトークンを選択するか決定する。

### Note/Tips

- 処理内容ごとに、適切なTemperatureを選択することが推奨される。
  - *Low (0.0-0.3)* : 一貫性が要る処理（例: Data extraction）
  - *Medium (0.4-0.7)* : 一般的なタスク全般（例: Summarization）
  - *High (0.8-1.0)* : 創造性が要る処理（例: Brainstorming）

## Supplement

- Temperatureは確率からの選定基準を定めるための物であって、異なる出力を保証するわけではないことに注意。
- 逆方向も成り立たない: temperature=0.0 でも完全な再現性は保証されない。memoの answer_low も2回目だけ末尾が違っており、その実例になっている。
- APIのデフォルトは `temperature=1.0`。明示的に渡さない限り最も創造的な設定で動くため、Factual/Coding用途では必ず下げる必要がある。

- 実践的なパラメータの一つであり、自身のサービスにfine-tuneする際に調節する。

## Reference

## memo

- 実装例。
  - 出力部分のみ、Notebookで何回か実行した。
  - answer_lowは1，3回目の出力が全く同じ、2もほぼ同じ。 answer_highはそれぞれ別の回答になっている。
    ```python
    def chat(
        messages: list[Optional[dict[str, str]]],
        system: Optional[str] = None,
        temperature: Optional[float] = 1.0
    ):
        params = {
            "model":model,
            "max_tokens":100,
            "messages":messages,
            "temperature": temperature
        }

        if system:
            params["system"] = system

        message = client.messages.create(**params)

        return message.content[0].text

    # Low temperature - more predictable
    answer_low = chat(messages, temperature=0.0)
    # output : answer_low
    # 1回目. '# エビングワースの忘却曲線\n\n**忘却曲線は、学習直後から急速に忘れ始め、復習のタイミングを最適化することで記憶を長期保持できることを示しており、効率的な学習スケジュール（1日後、3日後、1週間後など）の根拠となっています。'
    # 2回目. '# エビングワースの忘却曲線\n\n**忘却曲線は、学習直後から急速に忘れ始め、復習のタイミングを最適化することで記憶を長期保持できることを示しており、効率的な学習スケジュール作成の基礎となっています。**'
    # 3回目. '# エビングワースの忘却曲線\n\n**忘却曲線は、学習直後から急速に忘れ始め、復習のタイミングを最適化することで記憶を長期保持できることを示しており、効率的な学習スケジュール（1日後、3日後、1週間後など）の根拠となっています。'

    # High temperature - more creative
    answer_high = chat(messages, temperature=1.0)
    # output : answer_high
    # 1回目. '# エビングハウスの忘却曲線について\n\n**エビングハウスの忘却曲線は、復習のタイミング（1日後、1週間後、1ヶ月後など）を示す理論で、この間隔で復習することで長期記憶への定着を効率的に促進できます。**'
    # 2回目. '# エビングワースの忘却曲線\n\n**忘却曲線は、時間経過とともに記憶が急速に減少することを示しており、この曲線に基づいて最適なタイミング（1日後、3日後、1週間後など）で復習することで、記憶の定着を大幅に改善できます。**'
    # 3回目. '# エビングハウスの忘却曲線\n\n**人間は学習直後から急速に忘れ始めるが、定期的な復習によって忘却速度が遅くなるという理論で、これに基づいた間隔反復学習が記憶定着に非常に効果的です。**'
    ```