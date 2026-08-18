---
paths: ["src/api/**/*"]
---
# API規約
- すべてのエンドポイントはPydanticモデルでリクエスト/レスポンスを検証する
- エラーは必ずHTTPExceptionで返す