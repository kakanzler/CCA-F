# Introduction to projects

## Summary

Projectsは
- chat履歴、知識、任意の指示やトーンを記憶する限定された空間での作業領域(="self-contained workspace"。
- 関連資料などをその作業領域内にUploadして紐づけられるので参照させ続けられる
- context limitになってもRAGを起動させて10倍まで自動スケーリング可能
- チーム作業可能でメンバーを招待できる(claude for Work契約のみ)

いつ使うべきか
- ワンショットの質問(one-off question)ではなく、あるトピック/資料に関連する質問を何度かする時
- 回答に共通する制約（参照サイト、テンプレートの使用、Toneの固定）させたいとき
- チームで同じ文脈・知識ベースを共有しながら作業する時(claude for Work契約のみ)

### Note/Tips
- Claudeは簡易説明(brief description)を見ない。人間のための記載場所
- Visibility(claude for Work契約のみ)設定可能
- InstructionsはProject内でのClaudeのふるまい方を定義する(Tone、具体的な作業順番、回答のテンプレートなど)
- InstructionsでWorkflowの自動化も可能。例:「会議のトランスクリプトをUploadしたら、このテンプレートで構造化サマリーを作成する」
- Uploadするファイル名も具体的な名前に記載すること。Claudeは名前からも内容を推測する。また、ファイル名を参照するようClaudeに指示を出すとき、Claudeが特定しやすくなる
- Google Driveと連携してドキュメントを直接リンクすることも可能
- 包括的なProjectを立てるのではなく、特定の領域から必要に応じてProjectsを拡張していく方が望ましい
- Uplaodしたファイルも古い情報が残ると回答もそれを参照するのでUpdateするべき。
- ProjectをShareするときの許可レベルは3段階(claude for Work契約のみ)
  - 閲覧のみ: Projectの中身の閲覧・チャットは可能だが変更不可
  - 編集可: Instructions編集・資料のUpload・他メンバーの管理も可能
  - 所有者: メンバー招待に加え、組織全体へのProject公開も可能

## Reference

- [Introduction to projects](https://anthropic.skilljar.com/claude-101/383393)