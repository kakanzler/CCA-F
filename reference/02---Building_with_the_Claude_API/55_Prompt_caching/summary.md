# [Prompt caching](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287772)

## Summary

‐ **Prompt caching** : 計算リソースの再利用によるClaudeのレスポンス速度向上・コスト削減・自動最適化機能。
    - ClaudeはUserから入力を受け取ると大まかに以下のフローでOutputを生成する。この時に計算した途中経過を捨てずにCashに留め、似たようなリクエストの際に使いまわすという機能
      - Tokenization
      - Embedding
      - Context Analysis
      - Generating output text

- 有効に働いている場面
  - 同じドキュメントやコードに対する質問や編集などを繰り返しRequestするケース

## Note/Tips


## Supplement

- 制約
  - cacheは1時間だけ存在する
  - 同じContextの要求に対してのみ有効

- キャッシュの読み書きは非対称で、初回リクエストが cache write（書き込み）、以降のリクエストが cache read（読み出し）になる。つまり「1回目は得をしない、2回目以降で回収する」仕組み。
- 1時間で消えるため、同じ内容が「たまに」再利用される程度では効果が出ない。同一コンテンツが極めて高頻度で現れるワークフローでこそ有効。

## Reference

