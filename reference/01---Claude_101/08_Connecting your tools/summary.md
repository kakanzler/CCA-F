# Connecting your tools

## Summary

- Connector
  - Claudeが外部ツール・サービスに直接アクセスし、情報の読み取りとアクション実行の両方を可能にする機能（ファイル検索、ドキュメント取得、レコード更新など）
  - ConnectorはMCPを実装した接続手段であり、コネクタに許可を与えることでClaudeがアプリケーションを利用できるようになる。
  - 2種類
    - Web Connector: Google Drive、Notion、SlackなどのCloudサービスと連携
    - Desktop Extensions: Claude Desktopアプリ経由でローカルファイルやネイティブアプリに接続（**Webインターフェース不可、Desktopアプリ必須**）

### Note/Tips
- Connector一覧: [claude.ai/directory](https://claude.ai/directory) またはチャット欄の`+`ボタン > コネクタ
- セキュリティ
  - 権限はコネクタごとに個別設定・トグルで切り替え可能（Scoped access）
  - Claudeがアクセスできるのはユーザーがアクセスできる範囲のみ（他ユーザーのデータには不可）
  - 信頼できるソースのコネクタのみ使用すること（Skillsと同様）

## Reference

- [Connecting your tools](https://anthropic.skilljar.com/claude-101/383397)
