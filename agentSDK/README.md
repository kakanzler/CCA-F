# agentSDK

Claude Agent SDK の学習用ディレクトリ。TypeScript 版と Python 版の両方を含む。

## tree-structure

```
agentSDK/
├── .env                        # ANTHROPIC_API_KEY（gitignore 対象）
├── .venv/                      # Python 仮想環境（gitignore 対象）
├── AgentSDK.ipynb              # Python 版 SDK の実験ノートブック
├── requirements.txt
├── sdk_settings.json           # hello-world から --settings で読ませる設定ファイル
│
├── hello-world/                # TypeScript 版・最小構成 + PreToolUse フック
│   ├── hello-world.ts          # 本体。query() にオプションとフックを渡す
│   ├── package.json            # @anthropic-ai/claude-agent-sdk, tsx, zod
│   ├── tsconfig.json
│   ├── README.md               # 配布元の解説
│   └── agent/                  # エージェントの作業ディレクトリ（cwd）
│       └── custom_scripts/     # .js / .ts の書き込みを許可する唯一の場所
│           └── hello.ts        # 検証で生成されたファイル
│
├── hook_test/                  # Claude Code 本体のフック動作ログ
│   ├── test.md
│   └── test.log                # 変更時刻を追記したログ
│
└── research-agent/             # Python 版・マルチエージェント構成
    ├── research_agent/
    │   ├── agent.py            # ClaudeSDKClient + AgentDefinition のエントリポイント
    │   ├── prompts/            # lead_agent / researcher / data_analyst / report_writer
    │   └── utils/              # subagent_tracker, transcript, message_handler
    ├── .claude/
    │   ├── commands/           # スラッシュコマンド 5 種
    │   └── skills/             # executive-briefing, pdf（pdf は pypdf 用で本構成では未使用）
    ├── files/                  # 実行時に生成（.gitignore 対象）
    │   ├── research_notes/     # researcher の調査メモ .md
    │   ├── charts/             # data-analyst の matplotlib PNG
    │   ├── data/               # data_summary.md
    │   └── reports/            # report-writer の PDF
    ├── logs/                   # セッションごとの transcript.txt と tool_calls.jsonl
    ├── generate_report.py      # report-writer が実行時に生成した PDF 組版スクリプト
    ├── pyproject.toml
    └── README.md
```

## sumamry

### hello-world

TypeScript 版の最小構成。`query()` にオプションを渡して LLM へリクエストし、`PreToolUse` フックで書き込み先を制限する。フロントエンドは無く、assistant のテキストを `console.log` に流すだけの CLI。

実行方法（PowerShell）。`.env` の値がクォートで囲まれているため、除去してから環境変数に入れる必要がある。

```powershell
cd agentSDK\hello-world
Get-Content ..\.env | Where-Object { $_ -match '^\s*[^#\s].*=' } | ForEach-Object {
    $k, $v = $_ -split '=', 2
    Set-Item -Path "env:$($k.Trim())" -Value $v.Trim().Trim('"').Trim("'")
}
npx tsx .\hello-world.ts
```

#### フックの仕様

`Write | Edit | MultiEdit` の実行**直前**に割り込む。ブロック条件は AND 2 つ。

```
(拡張子が .js または .ts) ∧ ¬(custom_scripts 配下) → block
```

`.md` や `.py` は拡張子チェックで抜けるため、どこに書いても素通りする。守っているのはスクリプトの置き場所だけ。

| ファイル | 場所 | 判定 |
|---|---|---|
| `hello.ts` | `agent/` 直下 | ブロック |
| `hello.ts` | `agent/custom_scripts/` | 許可 |
| `note.md` | どこでも | 許可 |

#### 検証で分かったこと

| 項目 | 内容 |
|---|---|
| モデル指定 | `"opus"` などのエイリアスは SDK に古い ID が埋まっており 404。明示 ID（`claude-haiku-4-5`）を使う |
| Haiku の最新 | 4.5。`claude-haiku-5` は存在しない |
| `maxTurns` | 3 ではツール利用タスクが `error_max_turns` で中断。15 で完走 |
| `disallowedTools` | `Write` だけ塞いでも `Edit` に迂回される。族ごと指定が必要 |
| `Task` サブエージェント | `options.model` を**継承せず** `claude-sonnet-4-5` 固定。コストの大半を占めるため、不要なら禁止する |
| `systemPrompt` | 既定は空。未指定だとエージェントが cwd を認識できず、相対パスの解決に失敗する。`{ type: 'preset', preset: 'claude_code' }` で標準プロンプトが入る |
| `extraArgs` | プロンプトではなく CLI 引数に変換される（`{settings: X}` → `--settings X`）。`Options` 型に無いフラグを渡す抜け穴。未知フラグは起動時に exit 1 |
| `sdk_settings.json` | `effortLevel` は未対応キーで黙って無視されていた。思考量の制御は `maxThinkingTokens` を使う |
| `continue: false` | 会話を打ち切るため、ブロックされた Claude は再試行できずユーザーに聞き返して終了する |

#### フック戻り値の 2 形式

旧形式は打ち切り。新形式（`hookSpecificOutput`）は拒否理由をモデルに返して継続させられる。

```typescript
// 旧: セッションを打ち切る
{ decision: 'block', stopReason: '...', continue: false }

// 新: 理由を返して再試行させる
{ hookSpecificOutput: {
    hookEventName: 'PreToolUse',
    permissionDecision: 'deny',
    permissionDecisionReason: '...',
} }

// 新: 拒否せずツール入力を書き換える（自動リダイレクト）
{ hookSpecificOutput: {
    hookEventName: 'PreToolUse',
    permissionDecision: 'allow',
    updatedInput: { ...toolInput, file_path: '正しいパス' },
} }
```

#### 既知の粗

- `hello-world.ts` のパス判定が `startsWith` の文字列比較。`custom_scripts_backup/` のような接頭辞一致を通してしまい、相対パスが渡された場合は全部ブロックに倒れる。本来は `path.relative()` で判定すべき箇所
- `Write` / `Edit` / `MultiEdit` の分岐が同じ `toolInput.file_path` を読んでおり、1 行に畳める

### hook-test

Claude Code 本体（SDK ではない）のフック動作を確認した記録。`test.md` を編集するたび、`test.log` に日時とパスが追記される。

```
2026-08-09 15:31:05.190177 : modified C:\...\agentSDK\hook_test\test.md
```

編集の**後**に記録されている点が hello-world の `PreToolUse` と対照的。

### research-agent

Python 版のマルチエージェント構成。`ClaudeSDKClient` と `AgentDefinition` を使い、Lead Agent がサブトピックに分解して専門サブエージェントへ委譲し、最終的に PDF レポートを生成する。**PDF 生成まで完走を確認済み。**

| エージェント | 主なツール | 役割 |
|---|---|---|
| Lead Agent | `Task` / `Agent` | 分解と委譲のみ |
| Researcher ×2 | `WebSearch`, `Write` | Web 調査 → `files/research_notes/*.md` |
| Data Analyst | `Glob`, `Read`, `Bash`, `Write` | 指標抽出 → `files/charts/*.png`, `files/data/` |
| Report Writer | `Write`, `Glob`, `Read`, `Bash` | reportlab で `files/reports/*.pdf` |

**各段階はディスク経由で受け渡す。** 会話コンテキストではなくファイルが状態なので、途中で落ちても再起動して続きから再開できる（検索のやり直しが不要でコストを無駄にしない）。

#### 実行方法

```powershell
cd agentSDK\research-agent

Get-Content ..\.env | Where-Object { $_ -match '^\s*[^#\s].*=' } | ForEach-Object {
    $k, $v = $_ -split '=', 2
    Set-Item -Path "env:$($k.Trim())" -Value $v.Trim().Trim('"').Trim("'")
}

..\.venv\Scripts\python.exe -m research_agent.agent
```

- **必ず `research-agent/` から起動する** — `setting_sources=["project"]` が cwd の `.claude/` を読むため
- **`-m` 形式が必須** — `research_agent` は venv 未インストール。`python research_agent/agent.py` だと `sys.path[0]` がスクリプトの置き場所になり ImportError
- 依存追加は `uv pip install matplotlib reportlab`。**uv 製 venv には pip が入っていない**ため `python -m pip` は使えない

#### 検証で分かったこと

| 項目 | 内容 |
|---|---|
| **`allowed_tools` は効かない** | `["Task"]` と指定しても Lead が `Skill` / `ToolSearch` / `TaskList` / `SendMessage` / `Bash` / `Read` を実行した。**制限は `disallowed_tools` に書く**（hello-world で実効性を確認済み） |
| `Skill` はコンテキスト爆弾 | Claude Code 組み込みスキル（`claude-api` 等）は数万トークン規模。1回呼んだだけで `Prompt is too long` で落ちた |
| ツール名が `Task` → `Agent` | SDK 0.2.134 でリネーム。デモ側は `'Task'` で照合しており、サブエージェント検出が全滅していた |
| `python3` は罠 | pyenv シムを指し matplotlib / reportlab が無い。**venv の絶対パスを指定する**。相対パス（`../.venv/...`）はモデルが絶対パスに展開する際に階層を誤った |
| 同梱 pdf スキルは使えない | 中身は `pypdf`（既存 PDF の加工）の解説で、`reportlab`（生成）ではない。しかも `pypdf` は未インストール |
| Lead は各段階でターンを終える | 「Waiting for researchers」と言って制御を返す。ユーザーが `Continue` で促す運用になる |
| サブエージェントのモデル | `AgentDefinition` の `model` は尊重される。TypeScript の `Task` が Sonnet 固定だったのと対照的 |

#### プロンプト内の矛盾で止まった例

`researcher.txt` に **「書き出す前に WebSearch を 5-10 回」**という前提条件があった。コスト削減のため会話側で「検索は 2 回まで」と指示したところ、researcher は条件を満たさないと判断して `Write` を実行せず、パイプライン全体が空振りした。

指示の数値を下げるだけでは足りず、**前提条件そのものを外し、書き出しを無条件にする**必要があった。プロンプト中の「N 回やってから」という記述は、外部から回数を制限すると容易にデッドロックを生む。

#### この構成に加えた変更

| ファイル | 変更 |
|---|---|
| `agent.py` | モデルを `claude-haiku-4-5` に明示、`max_turns=15`、`disallowed_tools` 追加、report-writer から `Skill` 削除 |
| `lead_agent.txt` | サブトピックを 2 固定（例示も 4→2 に修正。**例示を直すのが最も効く**） |
| `researcher.txt` | 検索 5-10→2-3 回、書き出しを無条件化 |
| `data_analyst.txt` | Python を venv の絶対パスに、チャート 2-4→1-2 枚 |
| `report_writer.txt` | Python を venv の絶対パスに、pdf スキル参照を削除 |
| `message_handler.py`, `subagent_tracker.py` | `'Task'` → `('Task', 'Agent')` |

#### 実行結果（1回の完走）

```
files/research_notes/  .md 2件（各 5.6KB）
files/charts/          .png 3枚（1784x884）
files/data/            data_summary.md 6.8KB
files/reports/         claude_api_pricing_report.pdf 251KB / 4ページ
```

`logs/<session>/tool_calls.jsonl` に全ツール呼び出しが JSONL で残る。エージェント別・完了成否付きで、挙動の追跡にはこれが最も有用。


## Reference

- [anthropics / claude-agent-sdk-demos](https://github.com/anthropics/claude-agent-sdk-demos)
  - hello-world
  - research-agent
