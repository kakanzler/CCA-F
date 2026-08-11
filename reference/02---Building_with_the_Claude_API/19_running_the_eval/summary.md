# [Running the eval](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287743)

## Summary

- **evaluation pipeline**
  1. datasetからそれぞれのtest caseを取り出す。
  2. promptと結合する。
  3. claudeへ入力する。
  4. graderで評価する。

## Note/Tips

- 具体的なやり方
    ```python
    def run_prompt(testcase):
        # 2. promptと結合する。
        prompt=f"""
    Please solve the following task

    {test_case["task"]}
    """
        ...
        # 3. claudeへ入力する。
        result = client.message.create(prompt=pompt, ...)
        return result
    ...

    def run_test(test_case):
        output = run_pompt(test_case)

        # 4. graderで評価する。
        score = 10
        # score = grade_by_model(test_case, output) # SEE NEXT LECTURE

        return {
            "output" : output,
            "test_case" : test_case,
            "score" : score
        }

    # 1. datasetからそれぞれのtest caseを取り出す。
    def run_eval(dataset)""
        results = []
        for test_case in dataset:
            result = run_test(test_case)
            results.append(result)
        return results

    with opne("dataset.json", "r") as f:
        dataset = json.load(f)

    results = run_eval(dataset)
    ```


## Supplement

- パイプラインは「先に全体を通してから中身を埋める」順で作る。この段階では grader を未実装のまま `score = 10` とハードコードし、まず dataset → prompt → Claude → 結果収集の経路を成立させている。
- 同じ理由で prompt も意図的に最小（フォーマット指示なし）にしてある。その結果 Claude の出力は冗長になるが、それ自体が eval で検出したい対象であり、以降のプロンプト改善のイテレーションで直していく。

## Reference

