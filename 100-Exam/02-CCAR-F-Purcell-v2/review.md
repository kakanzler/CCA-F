# review

## Urgent

### Question 4.9 · Multiple choice · select ONE · Domain 1

You are choosing decomposition strategies for two workflows: a code review that always checks the same five aspects, and a production-incident investigation whose next step depends on what each finding reveals. Which pairing is right?

- A. Dynamic decomposition for both — adaptive plans subsume fixed ones, so the flexibility costs nothing in practice
- B. Prompt chaining for both — fixed steps are reproducible and easier to regression-test
- C. Prompt chaining for the predictable five-aspect review; dynamic adaptive decomposition for the investigation
- D. Dynamic decomposition for the review; prompt chaining for the investigation


-> 自信をもってDと回答してしまった。Dynamic decomposition が並列要素をParallelarization Workflowと解釈し、Code Reviewが依存関係を持つから、Chaining Workflowと解釈したため。
あ、選択肢を読み間違えたんだ。。

4.9
Correct: C
The selection rule: fixed sequential pipelines for predictable multi-aspect work, adaptive decomposition where the path emerges from intermediate findings. Each workflow gets the structure its uncertainty profile demands.
Why not the others: A pays adaptivity overhead on a task with no uncertainty; B forces an investigation to follow steps written before the evidence existed; D assigns each strategy to the workflow that defeats it.


### Question 4.10 · Multiple response · select TWO · Domain 1

You are writing AgentDefinition configurations for the productivity system's subagents. Which TWO statements about subagents are accurate? (Select TWO.)

- A. Subagents automatically inherit the parent agent's full conversation history
- B. Each subagent's AgentDefinition carries its own description, system prompt, and tool restrictions for its role
- C. Subagents can inherit the parent’s context by setting an inherit flag in their configuration
- D. Subagents do not share memory between invocations — needed context must be provided explicitly in the prompt
- E. Subagent tool restrictions apply only to MCP-provided tools, not to built-in tools such as Bash or Write


-> 自信をもってB,Cと回答してしまった。
解きなおすと、B,Dだとわかる。おそらくCのcontextを引き継げるというのをmemoryを引き継げると読み替えてしまったし、contextはそれぞれのAgentで固有なため、引き継ぐことはできないし、そんなflg設定はない。contextを引き継ぐ方法はあるのか？


4.10 — Correct: B, D
Two load-bearing facts: subagents are configured individually (description, system prompt, tool restrictions), and they are isolated — no inherited history, no memory across invocations, so context passing is always explicit.
Why not the others: A and C invert the isolation model — context never flows automatically and no inherit flag exists; E is false — restrictions bind built-in and MCP tools alike, as configuration rather than suggestion.


## Risky

### Question 2.4 · Multiple choice · select ONE · Domain 3

A new teammate's Claude Code sessions ignore the team's coding standards. You discover the standards live in your own ~/.claude/CLAUDE.md. What is the correct fix, and how do you verify it?

- A. Move the standards into the project-level CLAUDE.md checked into the repository, and use the /memory command to verify what a session loaded
- B. Have the teammate copy your ~/.claude/CLAUDE.md into their own home directory on their machine, then verify with /memory that the file loaded
- C. Add the standards to .claude/settings.json, which is checked in and applied to every teammate’s sessions
- D. Publish the standards as a /standards slash command teammates run at the start of each session


自信をもって、Cと選択している。
Aが正解。personalの.claudeをprojectにおいてチーム全員が従うようにしようというコンセプトは理解していたが、選択肢を読み間違えた。.claude -> ｃが正解！と早とちり。。これは.clude/settings.jsonなので違う話。CLAUDE.mdの話なんだから。。しかもBはそれを各メンバーのHomeDirに置くという話、、これは全然違う。。また早とちり。。Aが正解。/memory要らない⇒A除外が先行していた。。。/memory でメモリファイル(CLAUDE.md)がロードされているか検証するまでがが1セット。

2.4 — Correct: A
User-level configuration applies only to that user — it never travels via version control. Team standards belong at project level, and /memory is the diagnostic that shows exactly which memory files a session loaded.
Why not the others: B works once, then drifts with every future edit — hand-copied configuration is unshared configuration; C misuses settings.json, which carries permissions and tool settings, not standards prose; D makes always-relevant standards opt-in and forgettable.

### Question 3.6 · Multiple choice · select ONE · Domain 2

Every subagent currently receives the full 18-tool catalog. Logs show the synthesis agent attempting web searches and the search agent trying document parsing — with frequent wrong-tool selections everywhere. What is the correct redesign?

- A. Add a routing tool the agents call first, which returns the name of the correct tool to use
- B. Group the catalog by category, adding a category header to each tool’s description
- C. Write longer system prompts warning each agent about the tools it should ignore
- D. Scope each subagent’s tool set to its role — a handful of relevant tools each


自信をもって、Bと選択している。（Cは明らかに違うとも）

正しいToolを呼べていない問題解決方法としては、ToolのDescriptiongの情報があいまい、または不足しているか、Subagentが専門性に特化していないか、が考えられる。であればDが回答ではないか？

3.6 — Correct: D
Tool distribution is an architectural control: agents choose more reliably among 4–5 role-relevant tools than among 18, and tools outside an agent's specialization are misused precisely because they are available.
Why not the others: A adds a selection step to solve a selection problem — and the router itself must now be chosen correctly; B reorganizes the same oversized inventory; C asks prompts to fight an inventory problem configuration should fix.

### Question 3.7 · Multiple choice · select ONE · Domain 2

Subagents burn many tool calls just discovering what data exists — listing available document collections, probing for issue summaries, checking what schemas are present — before real work begins. Which MCP capability reduces this?

- A. Expose content catalogs (document hierarchies, issue summaries, schema listings) as MCP resources
- B. Increase the tool-call budget so exploration is affordable
- C. Hard-code the current data inventory into every system prompt
- D. Add a describe_available_data tool that every agent calls once at startup to fetch the current inventory

自信をもって、Dと選択して即答している。
Dは利用可能なデータを取得するToolを全Agentの最初の呼び出しで渡すというものだが、最初に渡すのはCatalog情報であってToolではないのでAが正解。

3.7 — Correct: A
MCP resources exist for exactly this: exposing catalogs of available content so agents start informed. Discovery becomes a lookup instead of a spelunking expedition of exploratory calls.
Why not the others: B pays for the inefficiency rather than removing it; C goes stale the moment the data changes; D rebuilds the same capability as a bespoke tool — resources are the protocol’s designed primitive for exposing content catalogs.

## middle

### Question 2.8 · Multiple choice · select ONE · Domain 1

You want to resume last week's refactoring session, but since then the team has merged substantial changes across the files it analyzed, so most of its tool results now describe code that no longer exists. What is the reliable approach?

- A. Start a new session seeded with a structured summary of the prior conclusions, since the stale tool results make resumption unreliable
- B. Resume the session as-is; Claude automatically detects file changes
- C. Resume the session and run /compact first, so the stale tool results are compressed before any new work begins
- D. Resume the session and ask Claude to re-read each changed file, correcting its stale understanding incrementally as it goes


DとAで悩んでDを選択していた。
ファイルがなかったりするならresumeするより新しくセッション作った方がいいのでは？と思った。しかし、前までのcontextをすべて失うのでさすがにD。まずresumeしてファイルの変更を取り込めばよい。

-> ちがう。古い情報が事実として残り続けてしまうのが大問題。新しいセッションで新しい事実をもとに、ただし前回の内容の結果(structured summary)だけはもちこみ、推論させるべきなのでAが正解

2.8 — Correct: A
The resumption tradeoff: resume when prior context is mostly valid; start fresh with an injected summary when tool results have gone stale. Heavily changed files put this squarely in the second case — keep the conclusions, discard the outdated evidence.
Why not the others: B assumes an automatic re-verification that does not happen — stale results sit in context as if true; C compresses the stale evidence, but a compacted falsehood is still false; D leaves contradictory old and new file states in one context and invites the model to blend them — workable for minor drift, not substantial change.

### Question 3.3 · Multiple choice · select ONE · Domain 1

The coordinator currently invokes the web search subagent, waits for completion, then invokes the document analysis subagent — doubling research latency even though the two tasks are independent. How do you run them in parallel?

- A. Have the coordinator emit both Task tool calls in a single response
- B. Enable streaming on both subagent invocations so their outputs interleave as they are produced
- C. Move both subagents to a faster model tier, cutting each task’s individual latency
- D. Have the search subagent spawn the document analysis subagent itself once its own work completes

AとBで悩んでいた。
BがStreamingを有効にするというものだが、よくわからずこれを選択していたかもしれない。Aがcoordinatorというmain agentからの両方のTASKを起動させる(emit)ということだから、Aが正解

3.3 — Correct: A
Parallel spawning is achieved by emitting multiple Task tool calls in one coordinator response rather than across separate turns — independent workstreams then execute concurrently.
Why not the others: B changes delivery, not scheduling; C shortens each task but still runs them end to end; D re-creates the sequential dependency one level down — the second Task still waits for the first.

### Question 3.4 · Multiple choice · select ONE · Domain 1

Your coordinator gives subagents rigid step-by-step procedures (“run these exact five queries in this order”). Subagents fail whenever a topic doesn't fit the script. How should coordinator prompts be designed instead?

- A. Make the procedures longer, covering more contingencies explicitly
- B. Give subagents the research goal only, omitting quality criteria so nothing unnecessarily constrains the approach they take
- C. Specify research goals and quality criteria — what a complete answer looks like — and let the subagent adapt its approach
- D. Route off-script topics back to the coordinator, which issues a revised procedure for each one

自信をもってCを選択していた
Aは明らかに違う。手順をながくしても無意味。Bはゴールのみを与えているがCriteriaがないので品質が保証されないのでNG,その点CはCriteriaも与えるので品質を保証しながらゴールへ迎えると判断したが、BもCもstep-by-stepなrigid procedureを保証しないのでNGでは？Dが正解か？

⇒ ちがう。問題はRigid procedureを与えたことでsubagentがFailしているのでその代替手段。Dは想定外(off-script)の内容をmain agentに戻すという策だが、質問の回答になっていないし、Scriptにfitしない場合はFailしてしまうので返せないし、subagentは要約しか返さないから中身がわからずmain agentでは対応できない。 Cなら品質を保証してgoalに向け処理してくれるからこれでいいんだ。

3.4 — Correct: C
Goal-and-criteria prompts preserve subagent adaptability: the coordinator defines success, the subagent chooses the path — which is why the agent (not a fixed script) is there at all.
Why not the others: A is an arms race against topic variety that scripts always lose; B removes the definition of success along with the script; D turns every novel topic into a coordinator round trip — the adaptability belongs in the subagent.

### Question 4.6 · Multiple choice · select ONE · Domain 3

Developers keep invoking your /generate-fixture skill bare, without the entity type and record count it needs, then get confused by the results. Which frontmatter option addresses this?

- A. context: fork, isolating the confusion in a subagent
- B. allowed-tools, restricting what the skill can touch
- C. A more detailed description block documenting the required parameters and their defaults
- D. argument-hint, which prompts for the required parameters when the skill is invoked bare

BとCで悩みCを選んでいた
Aのforkはagentを作って呼び出させる使わせる際に指定するものなのでこの解決にはならない。Dのargument-hintは見覚えがなかったので除外、BでToolの指定なので明らかに違うが、SKILLの作成で重要なパラメータ、CはよくあるDescirptionをちゃんと書こうという話。でCにしたが、この必要なパラメータがない場合の対処方法の解決策になっていない。消去法でDしかないか。。

frontmatter	役割
context: fork	冗長な出力をメイン会話から隔離
allowed-tools	使えるツールを制限(強制力あり)
argument-hint	引数なしで呼ばれたときにパラメータを促す

4.6 — Correct: D
argument-hint is the frontmatter mechanism for exactly this: skills that need parameters can prompt for them on bare invocation instead of running underspecified.
Why not the others: A isolates output, not input requirements; B constrains tools, not arguments; C documents the parameters for whoever reads the docs — the invocation still runs bare.


## Low

### Question 3.10 · Multiple response · select TWO · Domain 5

You are designing how the web search subagent behaves when its searches fail or return nothing. Which TWO behaviors are correct? (Select TWO.)

- A. On any failure, halt the workflow and surface the error to the operator, since partial research risks a misleading report
- B. Attempt local recovery for transient failures, and propagate unresolvable errors to the coordinator with any partial results
- C. Return empty results marked as success when a search fails, so downstream agents degrade gracefully instead of halting
- D. Standardize all failures to a single “search unavailable” status so the coordinator’s error handling stays simple
- E. Distinguish access failures (timeouts, service errors) from valid empty results (successful queries with no matches)


BとDでまよいEは即答できていたようだ。D, Eを選択した。
これはpropagateという単語を知らなかったからかもしれない。propagateは上位へ伝えるということ。Dはすべてsearch unavailableで丸めてしまうので原因なども全くわからない状態になってしまう。Bはcoordinatorにエラーとして伝わり、部分的な結果もえるのでこちらの方が処理全体として勝っている。

3.10 — Correct: B, E
Resilient error propagation is layered and honest: handle locally what is locally fixable, escalate the rest with context the coordinator can act on, and never conflate “the search broke” with “the search found nothing.”
Why not the others: A makes any single failure fatal when partial-result strategies exist; C is silent suppression — failure dressed as fact; D simplifies away the very context recovery decisions need.

### Question 6.10 · Multiple response · select TWO · Domain 5

Reviewer capacity covers only a fraction of extractions, so review attention must be routed where errors are likeliest. Which TWO practices form a sound routing design? (Select TWO.)

- A. Trust the model's raw self-reported confidence scores without validation
- B. Have the model output field-level confidence scores, then calibrate review thresholds against a labeled validation set
- C. Review a fixed random 5% of all extractions, keeping the sample unbiased
- D. Route to human review the extractions with low calibrated confidence or ambiguous source documents
- E. Prioritize the longest and most complex documents for review, since extraction difficulty rises steeply with length

Dは選択できていた。Cを迷って選択したが時間もなかったのが原因か。
Aはモデルの生レポートを信じるということで構成ナシのConfidenceを信じるのが設計としてはダメ。Eは優先度をつけるとあるが、すべて同じ長さで優先度Highのケースを考えれば意味がない設計になるのでだめ。BはValidationセットを用いて校正させたモデルのConfidenceレベルを記載するという策でReviewerの能力が低くてもここを見ればどこを重点的に見ればいいかがわかるので設計としては良さそうだ。Cは乱数まかせになるのでダメ。Dは自身がないものや曖昧なドキュメントの場合はHumanReviewにまわすのでよさそう。

6.10 — Correct: B, D
Calibration then routing: field-level confidence scores become meaningful once thresholds are tuned on labeled data, and review capacity flows to the calibrated-low-confidence and ambiguous-source cases where errors actually cluster.
Why not the others: A uses uncalibrated confidence — the known-unreliable version of the right signal; C spreads scarce capacity uniformly when errors concentrate — random samples measure error rates, they don’t route reviewers; E leans on a length proxy that correlates only loosely with error risk
