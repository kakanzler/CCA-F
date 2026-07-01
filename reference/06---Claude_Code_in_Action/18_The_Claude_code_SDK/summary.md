# [The Claude Code SDK](https://anthropic.skilljar.com/claude-code-in-action/312001)

## Summary

- Agent SDK(TypeScript/Python)を利用すると、自身のコードかpromtを送信するなどのClaude Codeの操作が可能になる
- インストール方法
    ```sh
    mkdir sdk-demo
    cd sdk-demo
    npm init -y
    npm install @anthropic-ai/claude-agent-sdk
    ```

### Note/Tips

- デフォルトの状態ではすべてのアクセスを許可するためCLIにおける `--allowedTools`に相当するオプションを以下のようにjsonのフィールドに含めることで指定することで機能を制限した上でPromptを送信する、などの処理が書ける。SDKの詳細はReferenceのURLを参照。
    ```js
    for await (const message of query({
    prompt,
    options: { allowedTools: ["Read", "Glob"] },
    })) {
    // ...
    }
    ```

## Supplement

allowedTools以外にも、カスタムsystem prompt・MCPサーバー・hooks・subagents・セッション再開などCLIができることは一通りサポートする。

## Reference

- [Agent SDK documentation](https://code.claude.com/docs/en/agent-sdk/overview)