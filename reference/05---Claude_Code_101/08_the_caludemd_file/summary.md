# The CLAUDE.md file

## Summary

- CLAUDE.mdをProjectのRootに配置することで特定の指示をClaudeに持続的に記憶させることができる
  - CLAUDE.mdがない場合はすべてゼロベースで情報を整理・理解するため、Claudeは情報を扱いにくく、推測などを含んだ結果になる可能性があるが、配置することで、セッションごとに毎回まずCLAUDE.mdを読んでくれ、Promptに追加される

### Note/Tips
- Claudeへのメモリの持たせ方は2階層に分かれる。
  - CLAUDE.mdはteamで共有されるべきで、ProjectのRootディレクトリに配置し、GitなどでVersion管理されるのが望ましい
  - 一方で、プロジェクトに共有するまでもない、ユーザーの個人用の設定は`~/.claude/`に配置するのが望ましい。ここに配置することでProjectに依らず、ProjectのVersion管理の外でClaudeは設定を読み込んでくれる。
- Claudeに参照させたいファイルがある場合は`@`でファイルパスを記載する。

- Claudeに対して何度か同じような修正指示を要している場合、CLAUDE.mdに状況と実行ルールを記載することで都度の修正指示を回避できる可能性が向上する
- プロジェクトを開始してからある程度開発を進め、いくつか個々修正必要だなという整理ができたところで`/init`でCLAUDE.mdにその内容を記すことで、必要最低限の情報に絞ることができ、CLAUDE.mdをコンパクトにできる。

## Supplement


## Reference

- [The CLAUDE.md file](https://anthropic.skilljar.com/claude-code-101/469795)
