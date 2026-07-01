# [Another useful hook](https://anthropic.skilljar.com/claude-code-in-action/312427)

## Summary

- Hooksには`PreToolUse`, `PostToolUse`以外に以下のHookの種類がある
  - `Notification` : ClaudeCodeが通知(ClaudeがToolを使おうとした際の許可など)を送信した際(またはClaude Codeがidle状態になってから60秒後)に実行するhook
  - `Stop` : ClaudeCodeがタスクを完了した際に実行するHook
  - `SubagentStop` : SubAgentが完了した際に実行するHook
  - `PreCompact` : `/compact`やContextWindowが一杯になった際のcompact処理時に実行するHook
  - `UserPromptSubmit` : ユーザーによるPrompt送信時(Claudeが処理するより前)に実行するHook
  - `SessionStart` : 新しいSessionが開始、または既存のセッションが再開される際に実行するhook
  - `SessionEnd` : Sessionが終了した際に実行するHook

- hookした際に起動するスクリプトのInputとかなるstdin inputは利用するhookによって異なり、stdinに含まれる`tool_input`というフィールドはその際に呼ばれたtoolによって異なる。(tool_name : `TodoWrite`が呼ばれたなら`todos`)

### Note/Tips

- hook時、どんな入力をスクリプトで処理するべきか理解するために、以下のヘルパーhookを作り、ログに出力してから設計する、という手段がある。

  ```json
  "PostToolUse": [ // Or "PreToolUse" or "Stop", etc
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "jq . > post-log.json"
        }
      ]
    },
  ]
  ```

## Supplement

- stdinのJSONには共通で`hook_event_name`（どのhookが発火したか）と`session_id`が含まれる。ヘルパーhookでログを見る際、この`hook_event_name`で種類を判別できる。

- ヘルパーhookの`jq . > post-log.json`は、stdinで渡ってきたJSONを整形して丸ごとファイルに書き出すだけの仕組み。本番の`command`を書く前に「実際に何が渡ってくるか」を確認するための足場であり、`PreToolUse`/`Stop`など任意のhookで同じ手が使える。

## Reference

