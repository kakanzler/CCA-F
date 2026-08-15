# AgentSDK

## Work

### 1. Overview<sup>[1](#ref1)</sup>

- `cladue_agent_sdk`に搭載されるもの
  1. ClaudeにはBuilt-in Tool

    |tool |機能|
    |---|---|
    |`Read` | サ行ディレクトリ内の任意のファイルを読み取る|
    |`Write` |新規ファイル生成|
    |`Edit` | 既存ファイルへの編集|
    |`Bash`| ターミナルコマンド、スクリプト、Git操作などを実行|
    |`Monitor` | バックグラウンドスクリプトを監視、各出力行ごとにイベント駆動|
    |`Glob`|パターン(**/*.tsなど)でファイル検索する|
    |`Grep`|正規表現でファイル検索|
    |`WebSearch`|現在の情報をウェブで検索|
    |`WebFetch`|ウェブページのコンテンツ情報を取得して解析する|
    |`AskUserQuestion`|複数選択オプション付きでユーザーに明確化の質問する|

  2. Hooks

     - 機能表

        |Hook Event|機能|
        |---|---|
        |`PreToolUse`|HookMatcherで指定したToolが発火され*る直前*に実行するイベント|
        |`PostToolUse`|HookMatcherで指定したToolが発火され*た直後*に実行するイベント|
        |`Stop`|Claudeでの処理が何かしらの理由で止まった際のイベント|
        |`UserPromptSubmit`|PromptがClaudeに送信された直後のイベント|
        |`PostToolUseFailure`|ツール実行の失敗時のイベント|
        |`PreCompact`|会話圧縮リクエスト時イベント|
        |`SubagentStart`|subagent開始時のイベント|
        |`SubagentStop`|subagent停止時のイベント|
        |`SessionStart`|PromptがClaudeに送信され、Session開始の直後のイベント(TypeScript限定)|
        |`SessionEnd`|Claudeから最終的な回答が送信され、Sessionが終了する直後のイベント(TypeScript限定)|

     - 補足: 他のTypeScript限定のHook Event
       - `PostToolBatch`・`MessageDisplay`・`UserPromptExpansion`・`Setup`・`TeammateIdle`・`TaskCompleted`・`ConfigChange`・`WorktreeCreate/Remove`
       - hooksのPriority順位: `deny` > `defer` > `ask` > `allow` ）

    - 使用方法

        ```python
        from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher
        ```

  3. Subagent
     - `query(options=ClaudeToolOptions())`にて、`allowedTools=["Agent"]`と許可することで、呼び出しを承認し、anget={}でagentを定義する。
        ```python
        for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                ...,
                allowed_tools=["Agent", ...],
                agent={
                    "code-reviewer": AgentDefinition(
                        description="",
                        prompt="",
                        tools=["Read", "Grep", "Grob", ...]
                    )
                }
            )
        )
        ```
  4. MCP
     - 以下のようなフォーマットで利用するMCPを定義する
        ```python
        for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                ...,
                mcp_server=[
                    "{mcp_server_name}": {
                        "command" : "npx",
                        "args" : [
                            "",
                            ...
                        ]
                    }
                ]
            )
        )
        ```
  5. session
     - 最初のメッセージに"session_id"が送付されるため、それを保存。
     - その後、`ClaudeAgentOptions(resume=session_id)`で同セッションでの会話としてClaudeにQueryを投げる。
        ```python
        from claude_agent_sdk import SystemMessage, ResultMessage

        async def session_test():

            session_id = None

            async for message in query(
                prompt=prompt,
                options=ClaudeAgentOptions(
                    allowed_tools=["Read", "Grep"]
                )
            ):
                if isinstance(message, SystemMessage) and message.subtype == "init":
                    session_id = message.data["session_id"]

            async for message in query(
                prompt=prompt,
                options=ClaudeAgentOptions(
                    resume=session_id
                )
            ):
                if isinstance(message, ResultMessage):
                    print(message.result)

        ```

  - 他Claudeツールとの比較表
    - vs Client SDK
      - Client SDKは直接APIを実行するため、レスポンスの処理などすべて自前で実装が必要。
      - Agent SDKはより使いやすく組み込まれている。特にTool Loopなどを自身で設計したくない場合は最適
    - vs Claude Code CLI
      - 機能は全く同じ
      - Claude Code CLIが最適なケース
        - インタラクティブな開発
        - 何度も同じ処理が来ることが想定されない場合
      - Agent SDKが最適なケース
        - CI/CDパイプラインの実装
        - カスタムアプリケーションの実装
        - 本番環境の自動化
    - vs Managed Agents
      - Managed AgentsはホストされたREST APIでAPIを呼び出す側とのステートフルな通信で実装される
      - 自身でsandboxを作ってsessionを管理するネットワークを設計する必要がないのがメリット。
      - 長時間セッションでの非同期通信も実現したいが、自身でネットワークを構築したくない場合最適

#### Supplement

- 権限がない状態で回すと以下のように言われる."Write", "Edit"を許可していても、同じタイミングで"Bash"などの権限が許可されていない場合にも下記エラーがでる可能性は高い。
    ```sh
    書き込み権限が必要です。承認していただければ `hook_test/test.md` に `# Claude here` を書き込みます。
    ```
- allowed_toolsの性質（許可であって拒否ではない）
  - `allowed_tools`は事前承認するツール群の指定であり、それ以外を拒否するわけではない。
  - *Permissonモード*や*canUseToolコールバック*を使うとリストにないToolも使用可能になる。
  - 使用を拒否したい場合は`disallowed_tools`で明示的に指定する必要がある。
- マッチャーはツール名のみで、ファイルパスではフィルタしない

### 2. Hook<sup>[2](#ref2), [3](#ref3)</sup>

- *典型的な使用例*
  - ログ・監査
  - 入力・出力の変換：サニタイズ・認証情報の注入
  - Userへの操作承認の要求
  - 状態管理：セッション内での状態管理・通知送信・リソース管理

- *Flow*
    ```mermaid
    stateDiagram
        イベントが発火 --> SDKが登録されたフックをsettingsとhookの名前から収集する。
        SDKが登録されたフックをsettingsとhookの名前から収集する。 --> HookMatcherがどのHookを実行すべきかをhookの名前をフィルタリングして決定する
        HookMatcherがどのHookを実行すべきかをhookの名前をフィルタリングして決定する --> コールバック関数を実行
        コールバック関数を実行 --> 最終的なResponse
    ```

### 3. Subagents<sup>[5](#ref5)</sup>

- subagentは3つの方法で作れる
  1. query()にagentsパラメータを使用する
    ```python
    for message in query(
        prompt=prompt,
        options=CaludeAgentsOptions(
            ...,
            allowed_tools=["Agent"],
            agent={
                "{agent_name}" : AgentDefinition(
                    "description"="...",
                    "prompt"="...",
                    "tools"=["Grep", ...]
                )
            }
        )
    ):
    ...
    ```
  2. ファイルシステムベース(`.claude/agents/...`)にエージェントを定義する
  3. built-inの一般的なAgent(`general-purpose`など)を使用する(Claude側の判断でいつでも実行可能)

- *メリット*
  - **コンテキスト分離**
    - Subagentはmain agentとコンテキストが分離され、処理結果の要約だけ返却するため、main agentのContext Windowを汚さずに済む
  - **並列処理**
    - 最終的な処理時間は各subagentの最も遅い処理に依存し、それらすべての合計ではなくなる
  - **専門性**
    - 各Subagentは専門的な処理やベストプラクティスをあらかじめ定義し実行可能。main agentでは柔軟性を捨てることになるため実装できないがsubagentなら一時的なタスク処理のために可能。
  - **Toolの使用制限**
    - 各Subagentが使用可能なToolを宣言できるため、不要な操作などを制限することでコスト・時間効率の向上、安全性の向上を担保して処理が可能。

- `AgentDefinition`:
  - 設定項目
    - 必須
      - *description* : `string` Agentをいつ使用すべきかの説明(自然言語)
      - *prompt* : `string` Agentの役割と呼び出す際の指示（システムプロンプト）
    - 任意
      - *tools* : `string[]` 事前許可するToolのリスト。デフォルトはすべてのTool
      - *disallowedTools* : `string[]` AgentのToolセットから削除する。(呼び出される可能性が0になる)。mcp_serverレベルも可能
      - *model* : `string` "haiku", "sonnet", "opus", "fable", "inherit"が有効。"inherit"は呼び出す側(main agent)と同じモデルを使用するということ
      - *skills*: `string[]` スタートアップ時にコンテキストにPreloadするSkillを登録する。ここで明記しなくとも、skill toolで呼び出すことは可能
      - *memory* : `user`, `project`, `local` : agentに利用するmemoryの位置
      - *mcpServers*: `(string | object)[]` subagentが利用可能なmcpサーバーの名前
      - *initilaPrompt* : subagentがmain thread agentとして自動送信される場合に渡されるprompt
      - *maxTurns* : subagent停止までの最大Turn数
      - *background* : 呼び出されたときに
      - *effort* :`string` "max", "xhigh", "high", "medium", "low", "number" から選択
      - *permissionMode*: `PermissionMode` "editAllow"で定義したPermissionMode型 など

- subagentが継承するもの
  - **AgentDefinition.prompt(唯一の継承チャネル)**, `Toolsの定義`, `CLAUDE.md`など(特に、このpromptが唯一のチャネルなのでのsubagentが処理にするにあたって必要なものはここで渡す必要がある。)
  - 特殊なケースとして; `SendMessage`というToolがAlloedToolsで許可されているSubagentは親からほかのsubgentのListを自動で継承する。subagent同士で会話するため。
- subagentが継承しないもの
  - 親のSystemPrompt, 親の会話履歴、親のツール結果, 親がpreloadしたスキル

- subagentがAPIエラーなどでエラーになってもそのメモがmain agentに返されるだけ

- subagentの呼び出し
  - subagentの呼び出し方は二通り
    - ClaudeがPromptの内容に基づき、subagentのDescriptionと照合し必要に応じて呼び出す
    - Promptで明示的に呼び出すようにClaudeに要求する
  - 呼び出されたかは `tool_use`ブロックで["Agent"]があるかをみる

- 再開
  - サブエージェントは結果をmainに返した後も会話履歴、ツールの呼び出し、推論、結果をすべて保持しており、resume可能。
  - resumeのFlow
    1. `for message in query():`の最初の`message`から、`sessionID`を取得する
    2. tool: Agent の結果に`agentId: <id>`をテキストブロックとして配置しているためこれを取得
    3. 再開する`query()`のoptionで `resume: sessionId`を割り当て、`prompt`に`AgentID`を含める。
    4. ※ カスタムエージェントを利用する場合は1度目も再開する際も`agentsパラメータ`に両方同じを割り当てる必要がある。

```python

def extract_agent_id(block: ToolResultBlock) -> None | str:
    parts = block.content if isinstance(block.content, list) else [{"text": block.content}]
    for part in parts:
        ### 正規表現解説
        # \s* : 0個以上の空白文字
        # ([\w-]+) : キャプチャグループ 1個以上の単語文字またはハイフン
        # \w : 単語文字(a-z, A-Z, 0-9, _)
        # - : ハイフン
        # + : 1個以上の繰り返し
        # agentId:   abc1-23 の場合 以下となる。
        # match.group(0) : agentId:   abc1-23
        # match.group(1) : abc1-23
        if match := re.search(r"agentId:\s*([\w-]+)"), part.get("text") or ""):
            return match.group(1)
    return None

# first query
for message in query(
    prompt=prompt,
    option=ClaudeAgentOptions(allowed_tool=["Grep", ...], agents=AGENTS)
):
    # get session_id
    if hasattr(message, "session_id"):
        session_id = message.session_id
    # get agent_id
    for block in getattr(message, "content", None) or []:
        if isinstance(block, ToolResultBlock):
            agent_id = extract_agent_id(block) or agent_id
    ...

# second query (resume)
if agent_id and session_id:
    async for message in query(
        prompt=f"resume agent {agent_id} and do something ...",
        options=ClaueAgentOptions(
            allowed_tool=["Grep", ...],
            agent=AGENT,
            resume=session_id
        )
    )
    ...
```
- subagentのcontext
  - subagentのContextはmainのcompactなどで影響を受けない。独立している。
  - sessionは永続するため、contextは保持される。しかし、デフォルト30日で自動でclean-upされる。CleanupPeriodDaysで指定可能。

- subagentの動的なscale-up
  - TypeScriptのAgent SDKでのみ有効だが、`allowedTools=["Workflow"]`と明記することで、Workflowを動的に実施することが可能。turn毎に数十～数百のagentを調整・実行する場合は特に有効。
  - これは*Parallelization*だけでなく、*Chaining Workflow*、*Routing Workflow*であっても有効 (*Optimizer-Evaluator*については具体例がなかったが、おそらく可能)

## Tips

- Cost最小化のための工夫

  1. `sdk_settings.json`に以下を指定し、ClaudeAgentOtionsで指定する
     - `sdk_settings.json`
        ```json
        {
            "model" : "Haiku",
            "effort" : "low"
        }
        ```
    - `main.py`
        ```python
        for message in query(
            prompt="xxx",
            options=ClaudeAgentOptions(
                permission_mode="acceptEdits",
                settings=str(Path("sdk_settings.json").resolve()),
                allowed_tools=["Write", "Edit"],
                disallowed_tools=["Task", "Bash", "WebSearch", "WebFetch", "Skill", "Workflow"],
                max_turns=3,
                hooks={
                    "PostToolUse": [
                        HookMatcher(matcher="Edit|Write",
                                    hooks=[log_file_change]
                                    )
                    ]
                }
            )
        )
        ```
    - キモ
      - settingsでsdk_settings.jsonを指定。
      - allowed_toolsで使用可能なToolを指定
      - disallowed_toolsで使用を禁止するToolを明示指定。コストにかなり効いた。
      - max_turns Claudeがapi側との通信する最大の往復回数の指定。Tool仕様の暴走を防ぐ。


## Reference

<a src="ref1"></a>

1. [Agent SDK の概要](https://code.claude.com/docs/ja/agent-sdk/overview)

<a src="ref2"></a>

2. [フックを使用してエージェントの動作をインターセプトして制御する](https://code.claude.com/docs/ja/agent-sdk/hooks)

<a src="ref3"></a>

3. [利用可能なフック](https://code.claude.com/docs/ja/agent-sdk/hooks#available-hooks)

<a src="ref4"></a>

4. [マッチャー パターン](https://code.claude.com/docs/ja/hooks#matcher-patterns)

<a src="ref5"></a>

5. [SDK のサブエージェント](https://code.claude.com/docs/ja/agent-sdk/subagents)