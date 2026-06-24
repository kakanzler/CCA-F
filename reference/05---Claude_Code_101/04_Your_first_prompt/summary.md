# [Your first prompt](https://anthropic.skilljar.com/claude-code-101/469791)

## Summary

- プロンプトの基本: 通常のAIアシスタント同様に、できるだけ具体的に記述する。詳細なほど意図が正確に伝わる

- `Shift + Tab` : Permission modeの切り替えが可能。
  - **Approval mode** モード
    - デフォルトの安全モード、必ず確認ステップをはさむ
  - **Auto-accept mode** モード
    - command以外のすべての操作は自動で承認される
  - **Plan** モード
    - read-onlyモード。自動で編集はしないが、どう編集すればいいのかを調査してくれる。調査の過程で適宜確認質問を行い、実行可能な詳細プランを提示する。安全なコードレビュー用途にも有効。


### Note/Tips

- モードは利便性と監視体制のトレードオフなので正解はないが、計画的に選択して実行するのが望ましい。
- `.claude/settings.json`に以下のように記載することでデフォルトのモードを指定可能
```JSON
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

## Supplement

- モードは何で立ち上げているかによって変わるようだ。
  - CLI
    - (Mode)
      - default (Approval mode)
      - acceptEdits (Auto-accept mode)
      - plan (Plan mode)
  - DesktopApp
    - UI label	(Mode)
      - Approval  (Approval mode)
      - Accept Edits (Auto-accept mode)
      - Plan (Plan mode)
      - Auto  (Auto mode)
      - BypassPermissions (Bypass Permissions mode)
  - VSCode
    - UI label	(Mode)
      - Ask before edits    (Approval mode)
      - Edit automatically  (Auto-accept mode)
      - Plan mode           (Plan mode)
      - Auto mode           (Auto mode)
      - Bypass permissions  (Bypass Permissions mode)

※ Auto Mode と Bypass permission Modeは
- Auto Mode: 長い処理時間を要するタスクなどに有効だが、Claudeが危険と判断すること以外はすべて実行されるため計画的に利用すること
- Bypass permission Mode : コンテナや仮想マシン内の操作をClaudeにさせる際に使う設定。利用には`Allow dangerously skip permissions`トグルを有効にする必要がある。


## Reference

- [Choose a permission mode](https://code.claude.com/docs/en/permission-modes)
- [Eliminate prompts with auto mode](https://code.claude.com/docs/en/permission-modes#eliminate-prompts-with-auto-mode)