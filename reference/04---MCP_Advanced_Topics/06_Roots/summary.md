# [Roots](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296289)

## Summary

- **Roots** : MCP serverにlocal内のフォルダ/ファイルへのアクセスを許可すること。
  - *大まかな流れ*
    1. UserがPrompt送信
    2. `list_roots`を呼び、アクセス可能なDirectoryを得る
    3. `read_dir`により、ファイルを探す
    4. 見つけたら、FullPathをContextに含め、`coversion tool`を呼ぶ

  - *security*
    - 許可したDirectory以下のファイルしかアクセスできず、その範囲外へのアクセスはErrorになる。さらにそのErrorを受け取って、Userへアクセス不可の旨を伝えられる

  - *実装の概略*
    - MCP SDKはRoot制限を自動強制しないため、`is_path_allowed()`のようなヘルパー関数を自作しファイル操作が必要な各Toolの冒頭で呼び出してチェックする(promptに直接埋め込ませてもよい)
    - 引数：`request_path`
    - 内容：
      1. 許可されたRoot(複数可)の一覧を取得
      2. 要求パスが許可Rootのいずれかの配下に収まるか判定
      3. アクセス可否(true/false)を返却する

### Note/Tips


## Supplement

- FileへのFULLPATHをClaudeに渡せば解決しそうだが、UXがよい状態とは言えない。その解決策にもなっている。

## Reference

