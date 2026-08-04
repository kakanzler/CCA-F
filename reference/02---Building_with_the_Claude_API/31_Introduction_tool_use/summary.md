# [Introducing tool use](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287747)

## Summary

- **Tools use** : Claudeが事前学習した情報だけでなく、最新データを授受したり、機能を拡張するために使われる。
  - Process
   1. Server側（ClaudeのAPIを叩く側）が、質問とあわせて「利用可能なTool」の定義を渡す
   2. Claudeが質問を分析し、追加情報が必要と判断したら、どのToolに何を渡してほしいかを要求する
   3. Server側がその要求どおりにコードを実行し、外部API/DBから情報を取得する
   4. Server側が取得した情報をClaudeへ返す
   5. Claudeが元の質問と取得データを合わせて最終回答を生成する

### Note/Tips

- Toolの仕様から回答を得るために必要な情報を知ることができ、不足情報があればClaudeからServer（User）に必要な値が*構造化された形*で問い直すことができる。

## Supplement

- Toolを使わない場合、Claudeは「最新の天気は分かりません」と答えるしかない。Tool useはこの「学習時点で知識が固定される」という制約を、外部から情報を注ぎ込む構造的な手順で回避する仕組み。
- Toolの定義（何が使えるか）は最初のリクエストに含めて渡す。Claudeは毎回Toolを使うわけではなく、質問を見て必要と判断したときだけ要求する。

## Reference
