# [Overview of Claude models](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287722)

## Summary

- Realtime処理ならHaikuがベスト（ただしHaikuはreasoning非対応なので、推論を要するタスクでは選べない）。高精度な推論を必要とするならOpus。そのどちらもバランスよく必要である場合はSonnetが望ましい。
- 性能 vs. コスト + 推論の速さはトレードオフなのでビジネスの特性に合わせて適切なモデルを選択するのが望ましい。

### Note/Tips


## Supplement

- Opus / Sonnet / Haiku は世代名ではなく、Intelligence ⇔ Cost/Speed という1本の軸上のポジションを表す階層名。コストとレイテンシは同じ方向に動くので、実質「知能を取るか、速さと安さを取るか」の一次元の選択になる。
- 代表的な用途（各1つだけ）: Opus = 大規模アーキテクチャ設計など長時間・多段の思考を要するタスク / Sonnet = 一般的なコーディングや文書作成 / Haiku = 高ボリュームで単純なテキスト処理（分類・抽出・モデレーション）。

## Reference

