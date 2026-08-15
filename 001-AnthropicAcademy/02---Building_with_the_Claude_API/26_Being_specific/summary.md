# [Being specific](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287740)

## Summary

- Guidelineを策定する
  - prompt下部にGuidelineを付け加える。※どれも動詞で始める。
    - *listing型*
      - 出力が備えるべき性質を列挙する。
        - 長さ・構造/フォーマット・含める要素・トーン/文体
        ```text
        Write ~~~

        Guideline:
        1. Keep ~~~
        2. Include ~~~
        3. Include ~~~
        ```
    - *step型*
        ```text
        Write ~~~

        Follow these steps:
        1. Brainstorm ~~~
        2. Pick ~~~
        3. Outline ~~~
        4. Brainstorm ~~~
        ```

## Note/Tips

- listing型はsafety netになるのでどんなpromptにも入れるべき。
- step型は複雑な問題の解決や、多角的な視点で考察させたいとき、また意思決定を要する場面で有用

- どちらとも組み合わせて使うとより強力なpromptになる。

## Supplement

- step型は「出力が備えるべき性質」ではなく「答えを出す前に踏ませる思考プロセス」を指定するもので、listing型とは指定する対象そのものが対になっている。

## Reference

