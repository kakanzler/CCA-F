# [Routing workflows](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287801)

## Summary

- **Routing workflows** : Applicationがユーザーの様々なリクエストをどのパイプラインに処理を流せばいいのかを特定し、処理するフロー
  - Step
    1. *Router* : まず要求がどんな類の要求かをカテゴライズするために一度Claudeにリクエストする。
    2. *Specialized Prompt* :  カテゴリに応じ、適切なPromptを要求するように振り分ける。Promptはその用途に特化したものにできるので汎化は不要で専門性に特化できるのがポイント。
  - flow
    ```mermaid
    sequenceDiagram
    participant A as Server
    participant B as Claude

        A ->> B : categorize this!
        B -->> A : this is {category}
        A ->> {each category} : {specialized prompt / tool / workflow}
        {each category} -->> A : {specialized answer}
    ```

## Note/Tips

- **XML tags / XML-style tags**：XMLのように構造化した情報として渡すことでClaudeが推論しやすくなる。<sup>[1](#ref1)</sup>
    ```xml
    Categorize the topic of a video into one of the listed categories:

    <topic>Python functions</topic>

    <categories>
    - Educational
    - Entertainment
    - Comedy
    - Personal vlog
    - Reviews
    - Storytelling
    </categories>
    ```

## Supplement

- 振り分け先はPromptに限らず、カテゴリごとに独自のworkflowやtoolsを持つ「パイプライン」単位にできる。ルーティングの本質は「入力を1つの特化パイプラインだけに流す」ことで、Parallelizationのように全経路へ流さない点が対比になる。
- Routingが有効なのは、カテゴリを明確に定義でき、かつ分類ステップのオーバーヘッドを特化処理の精度向上が上回るとき。分類自体がClaudeで安定して行える前提も要る。

## Reference

<a src="#ref1"></a>
1. [プロンプティングのベストプラクティス - XMLタグでプロンプトを構造化する](https://platform.claude.com/docs/ja/build-with-claude/prompt-engineering/claude-prompting-best-practices#structure-prompts-with-xml-tags)
