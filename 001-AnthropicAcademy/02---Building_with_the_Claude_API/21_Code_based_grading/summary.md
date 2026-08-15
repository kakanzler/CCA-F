# [Code based grading](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287737)

## Summary

- *Code Grader*
  - Format
    - Format は「要求されたコード種別だけを返しているか」という評価観点であり、その判定に使う validator を選ぶために test_case 側が `format` を持つ。そのため以下の形で test_case が作られる。
        ```json
        {
            "task": "~~~",
            "format": "python"
        }
        ```
  - Valid Sytax
    - Code Grader は静的な評価になり、意図通りかそうでないかなので 10 / 0で返却することになる。
        ```python
        def validate_json(text):
            try:
                json.loads(text.strip())
                return 10
            except json.JSONDecodeError:
                return 0
        ...
        ```

- code grader（Format / Valid Syntax）と model grader（Task Following）は評価軸が補完関係にあるため、前のLectureで取得したmodel basedのスコアと単純に加算平均する。これは両者に等しい重みを置くという既定の選択であり、何を重視するかによって重み付けを変えてもよい。
    ```python
    score = (model_score + syntax_score) / 2
    ```

## Note/Tips

- promptに以下のように具体的な情報を与えることでより期待通りの結果を得ることができる
  - python などのコードが欲しい場合。(余計なコメントや説明が不要な場合)
    ```
    * Respond only wiht Python,...
    * Do not add any comments or ommentary or explanation
    ```

## Supplement

- 重要なことはpromptを修正したことで、改善したのかどうかが客観的な指標のもとこ評価できること。
- assistant の prefill は `` ```python `` のように言語を決め打ちせず `` ```code `` とすることもできる。python / json / regex のどれを返させるかを事前に確定できない場合でも、生のコードだけを書き始めさせられる。

## Reference

