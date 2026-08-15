# [Defining tools with MCP](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296697)

## Summary

- Python用のSDKを使う場合`FastMCP`を利用することで1行でMCP Serverを初期設定可能。
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")
```

- Toolはデコレータ`@mcp.tool`を関数に付与することで定義,登録する。
  - `mcp.tool(name="", description="")`という構成で、toolの名前、とそのtoolが何をして、何を返す関数なのかをコンパクトに説明する。その際必要なパラメータは関数の引数で指定(型指定含む)し、`Field(description="")`クラスを用いてdescriptionに記載することで、どんな引数が入るのかClaudeに伝える。明確に記載するべし。
  - このデコレータにより、JSON Schemaが生成される(手動でJSON Schemaを作る必要がない！)
  - 関数内でerror handlingや、Toolの挙動、returnで値の返却を記載することで、Toolとしての挙動も定義できる。

### Note/Tips


## Supplement

- `Field`は`Pydantic`というライブラリのClass
- `Pydantic`は、Pythonの型ヒントを活用してデータの検証や設定管理を行うための強力なサードパーティ製ライブラリ
- `Field`の第一引数はデフォルト値の指定<sup>[1](#ref1)</sup>

- 型ヒントはJSON Schema生成だけでなく、Toolに渡された引数の自動バリデーションにも使われる。
- `@mcp.tool(name="...")`で指定するtool名はMCPクライアント（Claude）に公開される識別子であり、Python関数名（例: `read_document`）とは独立している。

## Reference

<src ref="ref1"></src>
1. [FastAPIにおけるPydanticを使ったバリデーションのまとめ](https://qiita.com/uenosy/items/2f6b1aa258018d3db76c)
