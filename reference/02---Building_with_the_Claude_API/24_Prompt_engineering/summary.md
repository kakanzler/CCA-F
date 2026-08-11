# [Prompt engineering](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287745)

## Summary

- **Iterative Improvement Process**
  - flow
    1. 目標を定める
    2. 最初のPromptを作成
    3. Evalを実施
       - このレクチャーでは前回やった自作のものではなく、`PromptEvaluator`というクラスを用いる。
        ```python
        # instanceを作る
        evaluator = PromptEvaluator(max_concurrent_tasks=3)
        # datasetを作成する
        evaluator.generate_dataset(
            task_description="Write a compact, consise ~~~",
            prompt_inputs_spec={
                "xxx": "~~~"
            },
            output_file="dataset.json",
            num_cases=3
        )
        # Evalの実施。
        # extra_criteriaでpromptがユースケースにとっての必要事項を満足しているのかを評価させることを確実にしている。
        results = evaluator.run_evaluation(
            run_prompt_function=run_prompt,
            dataset_file="dataset,json",
            extra_criteria="""
        The output should inclue:
        - ~~~
        - ~~~
        """
        )
        ```
       - 上記でEvalが終わると、resultsでスコアが取得できるとともに、HTMLのスコアレポートが出力される。
       - このレポートにはどの部分でPromptが機能しなかったのか、どんな改善が必要なのかが記載されているため、次の改善に具体的に繋げられる。
    4. **prompt engineering**でpromptを改善する
    5. 再度 Evalを実施

## Note/Tips

- `PromptEvaluator()`の引数max_concurrent_tasksは同時に処理可能なタスク数。
  - 多くすればするほど、並列処理数が増えるためResponseが早くなるが、その分APIのquataを使うのでむやみに大きくしないこと。最初は3など小さい値でやるのがよい。
- `evaluator.generate_dataset()`の引数num_casesも最初は2～3程度で小さく始め、最終的なValidationで増やす。
- promptも最初は意図的に単純でシンプルなpromptでベースラインを作ることから始める。

- Prompt engineeringは**繰り返して**改善していく作業であるということは重要で、promptpの改善は**1か所ずつ**実装して何が改善に寄与したかをクリアにしながら繰り返すことが重要である。

## Supplement


## Reference

