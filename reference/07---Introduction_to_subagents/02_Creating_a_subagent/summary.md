# [Creating a subagent](https://anthropic.skilljar.com/introduction-to-subagents/450699)

## Summary

- `/agents` : Running中のSubagent一覧をみたり、ライブラリに登録されたSubagentを選択したり、自身でSubagentを作成することができるコマンド
- 作成のステップ
  1. スコープを選択する
     - **Projectレベル** : 現在のディレクトリ下でのみ有効
     - **Personalレべル** : ユーザーのローカル全体で有効
  2. どのように作成するかを定義する
     - 手動で定義を書いてもいいが、Claudeにどのように動いてほしいかを伝え詳細や名前、System Promptなどを作成させてもいい。
  3. 権限範囲の設定
     - 以下の権限から必要な権限を任意の数選択する。デフォルトではすべてチェックされているから、不必要なものを外す形になる。
       - Read-only tools
       - Edit tools
       - Execution tools
       - MCP tools
       - Other tools
- Subagent作成後、Config fileが生成される。
  - Config fileは以下のようなフォーマットとなる

    ```markdown
    name: <AGENT_NAME> (ユニークな名前 Claudeから直接呼び出される。またはPromptで`@agent {AGENT_NAME}`でも呼び出せる)
    description: <WHEN_CLAUDE_SHOULD_CALL_THIS_SUBAGENT> (いつClaudeが呼び出すかの定義が書かれている。制約として1行で書く必要があり、改行を入れたい場合はエスケープした `\n` を使う。また、親Agentからの要求に依存して動く場合は`proactively`という文字列を含めて定義することでユーザーの明示的な指示がなくてもClaudeが自動でSubagentに委任するようになる。しかし、詳細な説明があるほうがClaudeの委任判断が正確になる)
    tools: <ENABLE_TOOOLS_FOR_THIS_AGENT> (SubagentがつかえるToolを列挙する)
    model: <LLM_NAME> (Haiku, Sonnet, Opus, Fableなど、Inheritを選び親AgentのLLMと同じものを選択することも可能)
    color: <COLOR_IN_CONVERSATION> (UI上の色)
    ---

    <DEFINITION_OF_THIS_SUBAGENT_AS_Prompt> (Subagentがどんなタスクをどう処理するのか、そしてどんな形で親Agentに返却すればよいのかを定義するPrompt。具体的な指示を書くべし。)
    ```

### Note/Tips

- 権限設定では不必要な権限を外すことが可能だが、何かの原因特定に際し、対称のファイルを読むだけでよい、と想定しRead-Only toolsのみにすることがあるかもしれないが、時にはコマンドを実行することもあるがその際にexecution toolsが有効になっていないと実行できないので、原因特定まで時間を要すことなどがあり得る。ので、何の権限が必要になるかは用途をよく吟味する必要がある

- Subagentを定義したのに動作していない場合はDescriptionをよく確認し、より具体的な例を追加したり指示を具体的にしたりすることでClaudeはSubagentを使うようになる可能性が高まる。

## Supplement

- YAML Front Matter: Markdownファイルのファイル冒頭に挿入される、そのMarkdownファイルのメタデータ。Suubagent特別ではなく、割と一般的に使われる挿入のされ方。書かれる情報は用途による。
- Config file は通常 `.claude/agents/<agent-name>.md` に保存される（Project スコープならプロジェクト配下）。

## Reference

