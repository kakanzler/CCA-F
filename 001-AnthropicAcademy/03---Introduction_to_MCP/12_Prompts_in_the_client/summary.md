# [Prompts in the client](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296692)

## Summary

- MCP Clientにおけるprompt機能の実装
  - `list_prompts()`
    - そのsession中に利用可能なprompt一覧を取得するメソッド
  - `get_prompt()`
    - Prompt名と引数(dict[str, str]で、Key, Valueのセット)を受け取り、該当するPromptに変数補間してFormat済みのPromptメッセージを取得するメソッド
  - Promptは以下二つの組み合わせで定義される
    - User
    - Assistant Message(Clientが使える補助的なメッセージ)

- 全体の流れ
  1. (事前準備)MCP ClientにMCP Serverの機能をラップした機能を実装する。
  2. (事前準備)`@mcp.prompt`で定義されたメソッドをMCP Serverで定義する。
  3. UserがPrompt(例：`/format report.pdf`)を送信する。
  4. 引数は該当するメソッドの引数として入力される。
  5. 洗練されたPromptがServerからClientへ返却され、AI Model(Claudeなど)に投げる準備が整う。

### Note/Tips

- 何度も送信されるPrompt, 複雑な処理のPromptなどをカスタムプロンプトとして定義することで、よりこの意義が高まる。

## Supplement

- テスト方法
  - 以下のコマンドで実行できるが、ANTHROPIC_API_KEYが必要。(＝課金する必要あるので省略した)
    ```sh
    uv run main.py
    ```
  - `/` と打つことで、利用できるカスタムプロンプトを一覧で取得
  - そのあとの引数を記載すると、autocompleteで利用できるファイルが一覧で出力される
  - これは`mcp_client.py`で`async`でメソッドを定義し、`await`で結果が返るまでこのco-routine(=このタスク)だけ一時停止し、制御をイベントループに返し(＝ノンブロッキングともいう)、他のタスクに処理をまわす設計、つまり**非同期の処理**となっているから、入力中にも値を受け取ることが可能となっている。

- {Prompt集合} = {Userが実際に送信するメッセージ集合} ∪ {事前に用意された会話例（few-shot 的な模範応答）などのメッセージ集合}

- 良いPromptの条件（origin 強調点）: 高品質・十分にテスト済み・Serverの目的に沿っていること。

## Reference

