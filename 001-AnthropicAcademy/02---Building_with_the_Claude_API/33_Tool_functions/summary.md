# [Tool functions](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287756)

## Summary

- *Tool*: Pythonで書かれた一つの関数のこと。

### Note/Tips

- **Best Practice**
  - 関数名、引数名は目的を示すようなわかりやすい名前にすること
  - 必要な引数が入力されているのか、必ずValidateすること（空じゃないか、など）
  - 例外処理によってエラーをその意味が分かりやすいようにだすこと。Claudeはそのエラーを受け取り、内容に応じてretryするか、などを判断できる。

## Supplement

- Toolは特別なクラスやデコレータを必要としない、ごく普通のPython関数でよい。「Toolを作る」＝「関数を書く」であり、それをClaudeが呼べるようにするのは次の段階（JSON schemaで関数の仕様をClaudeに説明する）の仕事。
- Validationの例: `get_current_datetime(date_format="%Y-%m-%d %H:%M:%S")` で `date_format` が空なら `ValueError` を投げる。実際にはまず起きないエラーだが、「引数を検証し、意味の分かるエラーを返す」というパターン自体を示すのが目的。

## Reference

 