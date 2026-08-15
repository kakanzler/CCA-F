# [Accessing resources](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296695)

## Summary

- MCP ServerからのResponse処理に関して
  - Responseの中身
    1. 対称のファイルの中身(raw text)
    2. MIMEの種類
      - この種類に応じて、データをどうparseさせるかを決定する.
      - 以下は例示されていたread_resource()。mimeTypeに応じてparse方法を変えている。
          ```python
          async def read_resource(self, uri: str) -> Any:
              result = await self.session().read_resource(AnyUrl(uri))
              resource = result.contents[0]

              if isinstance(resource, types.TextResourceContents):
                  if resource.mimeType == "application/json":
                      return json.loads(resource.text)

              return resource.text
          ```
    3. 他のメタデータ

  - 他のツールを呼び出すことなく、このResponseを使ってファイルをそのまま読み、そのままPromptに挿入しAIに送信するので、スムーズな通信が可能なのがポイント

### Note/Tips

- read_resource()を定義する際、pydantic.AnyUrlをImportすることで、URIに対応する型定義が可能
- また、mime_typeでApplication/jsonを指定するならimport jsonが必要
```python
import json
from pydantic import AnyUrl
```

## Supplement

- リソースの参照方法（入口）: CLIで `@` を入力するとオートコンプリートで利用可能なresourceが一覧表示され、矢印キー＋スペースで選択できる。選択されたresourceがReadResourceRequestとしてサーバへ送られ、read_resource()のuri引数に対応する。「どうやってresourceを指定するか」がこの `@` mention。

- result.contents はlist。通常1リクエストで扱うresourceは1つなので、先頭要素 contents[0] を取り出している。

## Reference
