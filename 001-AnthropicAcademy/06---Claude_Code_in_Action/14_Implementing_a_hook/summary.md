# [Implementing a hook](https://anthropic.skilljar.com/claude-code-in-action/312003)

## Summary

- この章では実際にReadツールを拒否するガードレールのHooksを作るプロセスが示されている。

- hooksで**READ**のみ拒否するHooks作成例
  - `settings.json`
    ```json
    {
    "hooks": {
        "PreToolUse": [
        {
            "matcher": "Read",
            "hooks": [
            { "type": "command", "command": "node $PWD/hooks/read_hook.js" }
            ]
        }
        ]
    }
    }
    ```
  - `read_hook.js`というここで呼び出すhookスクリプト
    ```js
    process.stdin.setEncoding("utf8");

    let input = "";

    process.stdin.on("data", (d) => (input += d));

    process.stdin.on("end", () => {
        const toolArgs = JSON.parse(input); // JSONのパース
        const readPath = toolArgs.tool_input?.file_path || "";

        if (readPath.includes(".env")) { // エラーハンドリング
            console.error("You cannot read the .env file"); // Claudeはstderrをメッセージとして受け取る
            process.exit(2);
        }
        process.exit(0);
    });
    ```

### Note/Tips

- Grep や Fetch, BashなどそれぞれのToolによって、返却されるJSONが異なる(それぞれのフィールドの値が異なる)ため、Hookスクリプトでパースする際に、それらをもれなく読み取る必要があるが、それぞれのパターンをカバーするには労力が要る。そのため、補足に書いたようにpermissions.denyで大元から権限を絞ることで統一的に実装するテクニックがある

## Supplement

‐ Hookでツール呼び出しをブロックする仕組みは「終了コード」で決まる。`process.exit(2)` で呼び出しを**ブロック**し、`process.exit(0)` で**許可**する。ブロック時にstderrへ書いた文字列がそのままClaudeに渡るメッセージになる（許可/通常時は何も表示されない）。
‐ PreToolUseはその名のとおりツールが**実行される前**に介入する。だからこそ`.env`の中身がClaudeに渡る前に止められる。

- permissions.denyで権限をより細かく書くことができ、PreToolUseで設定するガードレールと組み合わせて使用することが可能。どちらも`settings.json`に以下のように書く。<sup>[1](#ref1)</sup>
    ```json
    {
        "permissions": {
            "allow": ["Bash", "FileEdit"],
            "deny": ["Bash:rm"]
        },
        "hooks": {
            "PreToolUse": [...]
        }
    }
    ```

## Reference
<a src="ref1"></a>
１．[権限を管理する](https://code.claude.com/docs/ja/permissions#manage-permissions)
