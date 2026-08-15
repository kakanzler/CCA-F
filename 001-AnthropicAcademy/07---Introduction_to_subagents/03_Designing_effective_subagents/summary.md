# [Designing effective subagents](https://anthropic.skilljar.com/introduction-to-subagents/450700)

## Summary

- subagentsからのOutputが生産的になるためには4つのポイントがある
  1. descriptionの記載内容
     - 親agentからsubagentへのタスクの切り出す際、AgentがSubagentに何をさせたいのかを記述するプロンプト作成やそのSubagentをいつ呼び出すべきかにdescriptionの内容が参照されるため詳細に書くこと。
       - subagentからAgentに例えば、「Reviewにあたり正確なファイル名が必要」などと書くと、AgentはSubagentにpromtを渡す際に具体的なファイル名をわたすようになる。
  1. 構造的なoutput formatを記載すること
     - 構造的なoutput format(箇条書き)を記載することを推奨。理由はチェックリストのように項目ごとに実施すればいいので何をどこまでやればいいのかが明確であること、最後まで行けば終わりと停止点が分かりやすく、必要以上に推論が長くなってしまうことを防げるから。
  2. 処理する過程ではまったポイントの報告
     - output format の最後に `Obstacles Encountered: Report any obstacles encountered during the processes. This can be xxxxx`という項目を最後の箇条書きに追加することで、もしsubagentが障害に出会ったら要約にそれを含めて報告するようにできる。
  3. toolの適切な権限設定
     - 過分な権限を与えると、余分な影響が出てしまうので権限設定にはポイントがある
       - Read onlyな調査用のSubagentには`Glob`, `Grep`, `Read`を付与する
       - CodeをReviewするようなSubagentには`Bash`でコマンドをたたけるようにして, `git diff`をできるようにするべきだ
       - コードの修正までスコープに入るようなSubagentには`Edit`, `Write`を付与する必要がある


### Note/Tips



## Supplement

- 親Agentのシステムプロンプトには、各subagentの description だけでなく **name** も含まれる。どのsubagentをいつ起動するかは name + description の両方で決まるので、自動起動の制御を効かせたいときは name も調整対象になる。

 - subagentが処理中に見つけたworkaround(何かをするためには何かが必要だった、などの情報)は親Agentに返却される要約に含まれていてほしいが、含まれていない場合、親Agentが再び必要に迫られ調査することになってしまう。
- subagentが見つけた場合に親Agentに報告してほしい内容
  - 設定の問題や環境の特殊性
  - 処理する過程で明らかになった回避策
  - 特別なフラグや設定ファイルを必要とするコマンド
  - ライブラリの依存関係


## Reference


