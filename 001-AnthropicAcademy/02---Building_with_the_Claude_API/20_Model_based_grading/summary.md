# [Model based grading](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287742)

## Summary

- Evalの評価システム(grader)は、モデルの出力を受け取って測定可能なシグナル(通常は1〜10のスコア)を返すもので、実装は3種類ある
  1. Code graders
     - プログラム的にSyntaxに沿うか、意図通りの出力の長さか、Wordは入っているか・いないかなどを静的に評価する
  2. Model graders
     - 他のAIを(API callで)使って品質を動的に、完全性、有用性、安全性などを評価する。柔軟な評価が可能。ただしスコア単体を要求すると6前後に偏るため、strengths / weaknesses / reasoning を併せて出力させて根拠を言語化させる。
  3. Human graders
     - 人間に手動で評価させる。人間が評価するため柔軟性があるが多量の時間を消費してしまう。
     - 回答全体の質、網羅性、深さ、簡潔さ、関連性／適切さなどの評価には有用

- *評価指標*: あくまで今回の例。これは自身の用途に応じて適切な指標を設計し、適切なGraderを割り当てる。
  - format
    - Code Graderが有効(静的な評価で十分だから)
    - 説明などが伴ったテキストではなく、python, jsonなどの要求に応じたフォーマットで出力しているか
  - valid syntax
    - Syntaxが規約に沿っているか
    - Code Graderが有効(静的な評価で十分だから)
  - task following
    - Model Graderが有効(以下のような0/1で判断できない、柔軟性を要する評価が必要だから)
    - 直接的に、明確に解答できているか
    - 生成されたコードはUserの要求への解答として十分か、直接的に対処できているか


## Note/Tips

- 構造化出力全般に効く原則:「結論フィールドは、根拠フィールドより後ろに置く」
  - スコア単体を求めるとモデルが6前後の中庸に寄る。strengths / weaknesses / reasoning を score より前のフィールドとして出力させ、根拠を先に言語化させることでスコアを評価として妥当な数字で生成させている。
- ※ 逆順だと拠が書かれている分もっともらしく見えるのに中身は最初の直感のまま、という一番タチの悪い状態になる可能性があるため危険。

## Supplement


- 実装例
  - 以下のように JSONのスコアをprompt内で定義し、JSONで返すように指示している。
  - JSONにscore, reasoningといったFieldを持たせて構造化しているのでそれを取り出し、statistics.mean()で加算平均を算出している。
    ```python
    def grade_by_moel(test_case, output):
        eval_prompt = """
    You are an expert code reviewer. Evaluate ~~~

    Task : {task}
    Solution : {solution}

    Provide your evaluation as a structured JSON object with :
    - "strengths" : ~
    - "weaknesses": ~
    - "reasoning": ~
    - "score" : A number between 1-10
    """
        ...
        add_assistant_message(messages, "```json")
        eval_text = chat(messages, stop_sequences=["```"])
        return json.loads(eval_text)

    def run_test_case(test_case):
        output = run_prompt(testcase)
        model_grade = grade_by_model(test_case, output)
        score = model_grade["score"]
        reasoning = model_grade["reasoning"]
        return {
            "output" : output,
            "test_case" : test_case,
            "score" : score,
            "reasoning" : reasoning
        }

    from statistics import mean
    def run_eval(dataset):
        results = []
        for test_case in dataset:
            result = run_test_case(test_case)
            results.append(result)

        average_score = mean([result["score"] for result in results])
        ...
    ```

- model grader は多少気まぐれで、同じ出力でもスコアが揺れることがある。それでも一貫したベースラインにはなるので、プロンプトを改良したときの相対的な改善を追う指標として使う（絶対値そのものを信用する使い方ではない）。

?Summaryに書いた評価指標はあくまで例だよね。おそらく。
> 回答: その通りです。originでは「コード生成プロンプトであれば、こういう点に注目するとよい」という文脈で format / valid syntax / task following の3つが挙げられています。評価指標は普遍的なものではなく、評価対象のプロンプトのタスクに応じて自分で定義するもので、その指標ごとに「静的に判定できるか／柔軟な判断が要るか」で code grader と model grader を割り当てる、という考え方が本体です。


## Reference

