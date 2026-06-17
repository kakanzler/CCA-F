# Creating with artifacts

## Summary

- "artifacts" (成果物)とは、claudeが生成するものを指す。以下の特徴を持つ
  - 約15行以上
  - 利用者が使いまわししやすいとclaudeが判断したもの
  - 自己完結している複雑な内容で構成されるもの
  - 適切なOutput形式を持つ
    - Document
      - markdown, plain text, Word docs, PDF, PowerPoint, Excelなど幅広い形式
    - CodeSnippet
    - HTML
      - CSSやJavaScriptを埋め込んだ一つのファイル
    - SVG(ベクター画像形式)
      - Logo、iconなど
    - Mermaid diagrams
      - フローチャート、シーケンス図、ガントチャート、組織図など
    - React Component
      - ダッシュボードやゲームなども含むInteractiveなUI、Visualiseされたダッシュボードなど
- 作成方法
  - 文脈から自動で作成する
  - 「Artifactsを作って」と明示的に依頼する
- Artifact ウィンドウでできること
  - Preview（見た目）とCode（ソース）の切り替え表示
  - コンテンツのコピー
  - ファイルとしてダウンロード
- Share
  - **Copy / Download**: 個人利用や他チャネルでの共有に使用
  - **Claude for Work**: 組織内でArtifactを共有可能（チーム認証が必要）
  - **Publish（Free含む全プランで利用可能）**:
    - リンクを持つ誰でも（Claudeアカウント不要）アクセス可能
    - 公開されるのは選択したバージョンのみ。チャット履歴は非公開のまま
    - 他のユーザーが "remix"（自分のClaudeで開いて改変・発展）できる
    - いつでも共有解除可能
    - Googleなどの検索エンジンのクロール対象にはならない

### Note/Tips

- 具体的に指示するほど良い結果につながる。例：「予算トラッカーを作って」より「カテゴリ別に経費を入力でき、円グラフで内訳を表示し、予算超過時に警告が出る月次予算トラッカーを作って」のほうが良い
- **エンドユーザーを説明する**: 誰が使うかを伝えることでClaudeが適切な設計判断をしやすくなる（例：「新入社員向け」vs「エンジニアチーム向け」では結果が異なる）
- 同じデータを使ったチャートでも、目的や文脈が変われば見せ方が変わるので、やはり具体的な指示とともにArtifactを作るよう指示したほうが良い結果につながりやすい
- Artifact作成後に修正を加えていくことも可能（一度に一つずつ変更するとトラブルシューティングしやすい）
- Artifact作成を最初から考えていなくても、やりとりをしていった先で作成指示をすることも可能

## Reference

- [Creating with artifacts](https://anthropic.skilljar.com/claude-101/383394)
