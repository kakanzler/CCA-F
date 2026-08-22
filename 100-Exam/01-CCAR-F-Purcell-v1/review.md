
# review

## Question 1.7 · Multiple choice · select ONE · Domain 2

A refund request violates the returns window policy. The tool rejects it. Which error response enables the agent to handle this correctly with the customer?

- A. errorCategory: “business”, retriable: false, plus a customer-friendly explanation of the policy — so the agent explains the refusal rather than retrying it
- B. errorCategory: “transient” so the agent retries later, when the policy might differ
- C. An empty result marked as success, to keep the conversation positive
- D. A stack trace, so the agent has maximum detail

## 1.7
Correct: A
Policy violations are business errors: non-retryable by definition, and best paired with an explanation the agent can relay. The retriable: false flag prevents wasted attempts; the friendly description powers the customer conversation. CCAR-

1-7 refund関連の話でこういった機微な情報はretlyして誤った情報をでっちあげるなどは非常に危険なため、Policy違反があった場合は人が確認する必要があり、エラーを返す、saftyな対応が最も適している。

## Question 1.10 · Multiple response · select TWO · Domain 5

In long multi-issue sessions, the agent's later responses misquote refund amounts and order numbers because earlier details were condensed into vague summaries, while each lookup_order result dumps 40+ fields into context. Which TWO changes address this? (Select TWO.)

- A. Extract transactional facts — amounts, dates, order numbers, statuses — into a persistent case-facts block included in each prompt, outside the summarized history
- B. Increase max_tokens so responses can be longer
- C. Summarize even more aggressively to save space
- D. Trim each tool result to only the fields relevant to the current issue before it enters context
- E. Ask the customer to repeat key numbers periodically

## 1.10
Correct: A, D

The paired fix: protect precise transactional facts from lossy summarization by persisting them in a dedicated block, and stop the bloat at its source by trimming verbose tool outputs to relevant fields before they accumulate.
Why not the others: B controls output length, not context quality; C intensifies the exact failure mode — numbers dissolving into vagueness; E outsources the system's memory problem to the customer.

1-10はセッションが長くなっていくほど過去のやり取りがあいまいなものになり情報が失われていく現象を改善するための策として、各セッションにおいて、結果としてのSummaryとは別に①case-factsフィールドを用意しそこに事実を列挙するようにすること②Toolの内容とPromptの課題との関連性が高いもののみを残すように設計することが重要。


## Question 2.1 · Multiple choice · select ONE · Domain 3

You have a personal /scratch-notes slash command you use constantly, but it reflects your own workflow and should not appear for teammates when they pull the repository. Where does the command file belong?

- A. In .claude/commands/ in the repository, like all slash commands
- B. In the root CLAUDE.md under a # Commands heading
- C. In ~/.claude/commands/ in your home directory, where user-scoped commands live outside version control
- D. In .claude/rules/ with a paths glob matching your username

## 2.1
Correct: C

Command scoping mirrors intent: ~/.claude/commands/ holds personal commands visible only to you, while .claude/commands/ in the repo is shared with everyone via version control. A personal workflow tool belongs in the former.
Why not the others: A publishes a personal tool to the whole team; B is project context, not a command definition mechanism; D misuses path-scoped rules, which condition on edited file paths, not identity.

2-1 は単純に自分の環境でしか動かないようなCommandファイルだからProjectに置いてもメンバーが使えないから自身の環境、~/.claude/に置くべきだというだけだな。

## Question 2.10 · Multiple response · select TWO · Domain 5

During multi-hour codebase exploration sessions, the agent starts answering from “typical patterns” instead of the specific classes it discovered earlier. Which TWO practices counteract this context degradation? (Select TWO.)

- A. Switch to a model with a larger context window and continue accumulating
- B. Maintain a scratchpad file recording key findings as they are discovered, and have the agent reference it for subsequent questions
- C. Repeat important questions twice in the same message
- D. Ask the agent to be more specific
- E. Delegate verbose investigation (e.g., “find all test files”, “trace the refund flow”) to subagents that return summaries, keeping the main session's context for high-level coordination

## 2.10
Correct: B, E

Both practices manage what occupies the context: a scratchpad persists precise findings outside the degrading conversation, and subagent delegation keeps verbose exploration out of the main window entirely, returning only distilled summaries.
Why not the others: A postpones the same degradation at higher cost; C and D add more text to an already saturated context without removing any of the noise causing the problem.

2-10はAgentからの正確な情報の取得の仕方で、①Codebaseの全探索などのMainContextWindowを汚染するような冗長なTaskはAgentに移譲すること②subagentの有無に依らず、だが、正確な数値や事実は要約に溶かさずscratchpadに書き出し、必要なときに参照する

## Question 3.5 · Multiple choice · select ONE · Domain 1

Completed reports are coherent but shallow on some subtopics. You want the system to notice and repair its own coverage gaps before finalizing. Which orchestration pattern achieves this?

- A. Lower the bar: accept the first synthesis as final to control costs
- B. An iterative refinement loop: the coordinator evaluates synthesis output for gaps, re-delegates to search and analysis subagents with targeted queries, and re-invokes synthesis until coverage is sufficient
- C. Ask the report generation agent to pad thin sections with general knowledge
- D. Always run every subagent exactly twice regardless of output quality

3.5
Correct: B
Iterative refinement closes the quality loop: evaluate coverage, dispatch targeted follow-up research where gaps exist, re-synthesize — repeating until the report meets criteria rather than hoping the first pass suffices.
Why not the others: A ships the known defect; C fills gaps with uncited generalities — the opposite of a cited research product; D doubles cost blindly with no gap-detection to aim the second pass.

3-5 単純に解答が望んでいる詳細情報や完了条件を満たしていない場合のWorkflowの選択なので、これはOptimizer - Grater Workflowの Feedback loopを実現する iterative refinement loop(B)が正解

## Question 3.8 · Multiple choice · select ONE · Domain 5

Final reports state findings but cite nothing. Investigation shows each summarization step compresses source attribution away, so by synthesis time nobody knows which claim came from where. What is the structural fix?

- A. Have the report generator add plausible citations at the end
- B. Instruct the synthesis agent to write “sources available on request”
- C. Require subagents to output structured claim-source mappings (claim, evidence excerpt, source URL or document name) that every downstream agent preserves and merges through synthesis
- D. Reduce the number of summarization steps to one

3.8
Correct: C
Provenance survives only if it is structural: claim-source mappings travel as data through every hop, so synthesis merges attributed claims instead of anonymous assertions. Attribution is preserved, never reconstructed.
Why not the others: A invents citations — worse than none in a research product; B advertises attribution the system no longer possesses; D reduces compression events but the remaining one still strips attribution.

3-8
各サブエージェントの出力段階から、claim と evidence/source を構造化データ(単なるプローズでなく)として保持し、synthesis を経ても失わせない。表示は結果であって、設計の要点はデータが**生き残ること。**

# Scenario 5: Claude Code for Continuous Integration

## Question 5.1 · Multiple choice · select ONE · Domain 3

Your CI job must run Claude Code non-interactively and produce review findings your pipeline can parse and post as inline PR comments. Which invocation is correct?

A. claude “review this PR” piped through grep to extract findings from prose
B. claude -p “review this PR” with --output-format json and --json-schema, producing machine-parseable structured findings without waiting for interactive input
C. claude --batch “review this PR” --format=structured
D. claude -p “review this PR” alone, then regex-parsing the prose output

## 5.1
Correct: B

The CI trio: -p (--print) for non-interactive execution, --output-format json for machine-readable output, and --json-schema to enforce the findings structure your pipeline consumes — no prose parsing, no input hangs.
Why not the others: A hangs waiting for interactive input and then scrapes prose; C invents flags that do not exist; D solves the hang but leaves the pipeline regex-parsing unstructured text.


Question 5.2 · Multiple choice · select ONE · Domain 3
CI-generated tests ignore your team's fixture library, duplicate helper setup, and test trivialities. Developers reject most of them. What is the configuration-level fix?
A. Generate three times as many tests so some survive review
B. Have developers rewrite the generated tests as a standing chore
C. Lower the temperature of the generation call
D. Document testing standards, what makes a test valuable, and the available fixtures in CLAUDE.md — the mechanism that supplies project context to CI-invoked Claude Code


5-1
Claudeに対話的な回答をさせずにすぐ答えだけほしい時、 claude -p というオプションでSTDIOで出力可能。 --output-format json　とすればJSON形式で出力させられるため、これをdumpしてJSON形式で受け取ることが可能(machine readble)。さらに--json-schemaのオプションにより、3-8のように推論で得たい知見をJSON-schema で定義した形式・内容を強制することができる。


## 5.2
Correct: D
CI invocations get their project context from CLAUDE.md. Standards, value criteria, and fixture documentation there directly raise generation quality — the model can only follow conventions it has been shown.
Why not the others: A scales the reject pile; B institutionalizes rework instead of fixing its cause; C reduces variability of output that is uninformed either way.




Question 5.3 · Multiple choice · select ONE · Domain 3
Reviews re-run after each new commit to a PR, and the bot re-posts the same findings every time — developers now mute it. How should re-reviews be designed?
A. Include the prior review's findings in context and instruct Claude to report only new issues or previously reported ones that remain unaddressed
B. Review only the newest commit's diff in isolation
C. Limit reviews to one per PR regardless of subsequent commits
D. Post all findings again but formatted differently to seem new





## 5.3
Correct: A
Duplicate suppression is a context design problem: give the reviewer its own prior findings and the explicit instruction to report deltas — new issues plus unresolved carryovers — and the noise stops while coverage remains complete.
Why not the others: B misses issues that emerge from interaction with earlier commits; C leaves everything after the first push unreviewed; D disguises the spam developers already muted.


## Question 5.4 · Multiple choice · select ONE · Domain 3

You notice that when the same Claude Code session that generated a change also reviews it, the review is conspicuously gentle — missing issues an independent reviewer catches. Why, and what is the design implication?

- A. The model is being polite; instruct it to be harsher
- B. Reviews should always be performed by a larger model tier
- C. A session retains the reasoning context from generation, making it less likely to question its own decisions — so CI reviews should run in an independent instance without the generator's context
- D. Generation and review must run on different days to avoid contamination



## 5.4
Correct: C
Session context isolation matters for review integrity: the generating session carries the rationale that produced the code, biasing it toward its own choices. An independent instance evaluates the code on its own terms.
Why not the others: A misreads a context effect as a personality setting; B changes capability when the problem is contaminated context — the same model reviews well when independent; D adds superstition to a mechanism that is about context, not calendars.

Question 5.5 · Multiple choice · select ONE · Domain 4
Your review prompt says “be conservative and only report high-confidence findings,” yet false positives remain high. What does effective precision engineering look like instead?
A. Add “be very, very conservative” for stronger emphasis
B. Report all findings but sort them by the model's stated confidence
C. Reduce the number of files reviewed per run
D. Replace confidence language with explicit categorical criteria: define which issue types to report (bugs, security) and which to skip (minor style, local patterns), with concrete

5-4
自身が推論した内容をReviewさせてもClaudeが客観的に評価できない(自身のOutputを自身で疑問視する可能性は低い)ため、agentなどの同じContextWindowを持たないモデルでReviewさせる必要がある、という話。

## 5.5
Correct: D
Vague conservatism doesn't transfer — specific criteria do. Defining reportable versus skippable categories with concrete boundaries gives the model an operable decision rule, which is what actually moves precision.
Why not the others: A intensifies an instruction that has no operational content; B reorders noise instead of reducing it


Question 5.6 · Multiple choice · select ONE · Domain 4
Findings in the “code style” category are 70% false positives, and developers have begun dismissing security findings too — trust in the whole reviewer is collapsing. What is the right operational move?
A. Ship more style findings to demonstrate the category's importance
B. Temporarily disable the style category to restore trust in the accurate categories, while improving the style prompts before re-enabling it
C. Rename “code style” to “code quality”
D. Ask developers to be more tolerant of noise during the tuning period


## 5.6
Correct: B
High false-positive categories are contagious: they teach developers to dismiss everything. Disabling the offender protects the credibility of accurate categories while its prompts are fixed offline — trust is the system's real asset.
Why not the others: A doubles down on the noise destroying trust; C relabels the same false positives; D asks humans to absorb a cost the configuration should eliminate.


Question 5.7 · Multiple choice · select ONE · Domain 4
The reviewer labels near-identical issues “critical” one day and “minor” the next. Severity-based merge gates are therefore unreliable. How do you get consistent severity classification?
A. Define explicit severity criteria with concrete code examples for each level, so every severity has an operational definition the model can match against
B. Remove severity levels and treat all findings equally
C. Let the model choose severity freely but average it over five runs
D. Map severity to line count of the affected code



## 5.7
Correct: A
Consistency comes from operational definitions: severity levels anchored by concrete examples give the classifier something to match, turning a vibe into a rubric. That is what makes severity gates dependable.
Why not the others: B discards the signal the merge gate needs; C statistically launders an unanchored judgment; D measures size, not impact — a one-line auth bypass outranks a fifty-line comment tweak.

Question 5.8 · Multiple choice · select ONE · Domain 4
The reviewer keeps flagging your codebase's accepted idiomatic patterns (e.g., intentional fall-throughs with comments) as bugs, while your detailed prose instructions haven't fixed it. What is the most effective addition?
A. A rule that anything containing a comment is acceptable
B. An instruction to “use good judgment about idioms”
C. Few-shot examples distinguishing the accepted patterns from genuine issues — showing the reasoning why each is or isn't reportable — so the model generalizes the judgment to novel cases
D. A ban on reviewing files containing any idiomatic pattern



## 5.8
Correct: C
When prose fails to convey a judgment boundary, examples carry it: contrasted acceptable-versus-genuine cases with reasoning teach a distinction the model can generalize — the documented strength of few-shot prompting for false-positive reduction.
Why not the others: A creates a trivially wrong rule any commented bug defeats; B restates the goal without transferring the judgment; D exempts exactly the code that most needs reviewing.


Question 5.9 · Multiple response · select TWO · Domain 4
Your team is deciding which CI workloads to move to the Message Batches API for its 50% cost savings. Which TWO statements are accurate? (Select TWO.)
A. Batch processing suits latency-tolerant, non-blocking workloads like nightly test generation and weekly audit reports
B. Batches are guaranteed to complete within one hour
C. The batch API supports multi-turn tool calling within a single request
D. Blocking workflows such as pre-merge checks should stay on the synchronous API, since batches can take up to 24 hours with no latency SLA
E. Batch responses cannot be matched back to their requests

## 5.9
Correct: A, D
The batch decision rule in both directions: overnight and weekly jobs are the ideal profile for the discount; anything a developer waits on cannot tolerate a 24-hour, no-SLA window and stays synchronous.
Why not the others: B and C are false — there is no latency guarantee, and mid-request tool execution is unsupported; E is false — custom_id exists precisely to correlate request/response pairs.

Question 5.10 · Multiple response · select TWO · Domain 4
You are adding few-shot examples to the review prompt. Which TWO practices reflect how few-shot prompting works best? (Select TWO.)
A. Include as many examples as possible — twenty or more — to cover every case
B. Use 2–4 targeted examples aimed at the ambiguous scenarios, showing the reasoning for why one action was chosen over plausible alternatives
C. Once examples are added, explicit criteria become unnecessary
D. Rely on examples only for prose tasks; they don't work for code
E. Include examples demonstrating the exact desired output format — location, issue, severity, suggested fix — to achieve consistent, actionable findings

## 5.10
Correct: B, E
Effective few-shot work is targeted and demonstrative: a handful of examples aimed at genuine ambiguity, with reasoning shown, plus format demonstrations that lock output structure — quality of targeting over quantity.
Why not the others: A bloats context and dilutes the signal of the examples that matter; C and D are false — examples complement explicit criteria, and code review is a prime few-shot use case.

# Scenario 6: Structured Data Extraction



Question 6.1 · Multiple choice · select ONE · Domain 4
Your current pipeline asks Claude to “respond with JSON” in plain text; downstream parsing breaks on markdown fences, trailing commentary, and occasional malformed syntax. What is the most reliable structural fix?
A. Strengthen the prompt: “respond ONLY with valid JSON, no exceptions”
B. Post-process the text with regexes that strip fences and repair syntax
C. Define the extraction as a tool whose input schema is your JSON schema, and read the structured data from the tool_use block — guaranteeing schema-compliant output and eliminating JSON syntax errors
D. Switch to XML output, which models format more carefully



## 6.1
Correct: C
Tool use with JSON schemas is the reliability mechanism for structured output: the model's extraction arrives as schema-conformant tool input, not as prose that happens to contain JSON — syntax errors are eliminated by construction.
Why not the others: A improves the odds within a fundamentally text-shaped channel; B patches symptoms with fragile repairs; D relocates the same free-text problem to a different syntax.


Question 6.2 · Multiple choice · select ONE · Domain 4
You have several extraction tools — one per document type — and incoming documents of unknown type. The model must always produce a structured extraction, choosing the appropriate schema itself, and never reply with conversational text. Which tool_choice setting is correct?
A. tool_choice: “any” — the model must call a tool but may choose which, guaranteeing structured output while leaving schema selection to the model
B. tool_choice: “auto” — the model decides whether to call a tool at all
C. tool_choice forced to one named tool, applied to every document
D. Omit tool_choice, since defaults handle this


## 6.2
Correct: A
The three modes map to intent: “any” compels a tool call while preserving the model's choice among schemas — exactly right for unknown document types that must always yield structured output.
Why not the others: B (and D, which defaults to it) permits conversational text instead of a tool call; C welds every document to one schema when types vary.


Question 6.3 · Multiple choice · select ONE · Domain 4
Your invoice schema marks vendor_tax_id as required. On invoices that genuinely lack a tax ID, the model fabricates plausible-looking values to satisfy the schema. What is the schema-level fix?
A. Add a prompt instruction: “never fabricate tax IDs”
B. Post-validate tax IDs against a checksum and discard failures
C. Lower the temperature to make fabrication less creative
D. Make the field optional/nullable so the model can legitimately return null when the information is absent from the source document

## 6.3
Correct: D
Required fields on possibly-absent information force fabrication — the schema leaves no honest answer. Nullable/optional fields give the model a legitimate way to say “not present,” which is the designed prevention for this failure.
Why not the others: A pits an instruction against a structural requirement that demands a value; B catches well-formed fabrications only by luck; C makes invented values more conservative-looking, not less invented.

Question 6.4 · Multiple choice · select ONE · Domain 4
Since adopting tool use, extractions are always syntactically valid — yet invoices arrive where line items don't sum to the stated total, and values occasionally land in the wrong fields. What should you understand and do?
A. Schema compliance was falsely advertised; file a bug
B. Strict schemas eliminate syntax errors but not semantic ones — add semantic validation, e.g., extracting calculated_total alongside stated_total and flagging discrepancies with a conflict_detected boolean
C. Make every field an unconstrained string so nothing can be wrong
D. Re-run each extraction until the numbers happen to sum


## 6.4
Correct: B
The boundary of the guarantee: tool use ensures structure, not truth. Semantic errors — sums that don't reconcile, transposed fields — need a semantic validation layer, with self-check fields like calculated_total making discrepancies machine-visible.
Why not the others: A misunderstands what was promised: shape, not semantics; C destroys the structure that downstream systems depend on; D retries until errors align by chance rather than detecting them.


Question 6.5 · Multiple choice · select ONE · Domain 4
An extraction fails Pydantic validation with two specific field errors. You will retry. What should the retry request contain — and when would you skip retrying altogether?
A. Just the instruction “try again more carefully”; skip retries on Mondays
B. Only the validation errors, to keep the retry cheap; always retry at least five times
C. The original document, the failed extraction, and the specific validation errors — enabling targeted self-correction; skip retrying when the required information is simply absent from the source, since no retry can produce it
D. A different document, to give the model a fresh start

## 6.5
Correct: C
Retry-with-error-feedback works because the model sees what it produced, what was wrong, and the source to correct against. And the boundary matters: format and structural errors are retryable; information absent from the document is not.
Why not the others: A retries blind — the model can't fix errors it isn't shown; B removes the document and extraction the correction must reference; D abandons the failed extraction rather than repairing it.


Question 6.6 · Multiple choice · select ONE · Domain 4
An overnight batch of 10,000 documents completes with 200 failures: most are oversized documents that blew past context limits, plus some transient errors. What is the correct failure-handling workflow?
A. Identify the failed requests by custom_id and resubmit only those, with modifications where needed — e.g., chunking the oversized documents before resubmission
B. Resubmit the entire 10,000-document batch and keep whichever results arrive first
C. Discard the 200 failures as an acceptable loss rate
D. Switch the 200 failures to the synchronous API unchanged, where context limits don't apply

## 6.6
Correct: A
custom_id exists for exactly this: correlate failures to their source documents, fix what caused each failure (chunk the oversized ones), and resubmit only the fixed subset — paying again for 200 documents, not 10,000.
Why not the others: B reprocesses 9,800 successes to retry 200 failures; C silently drops 2% of the corpus; D misunderstands context limits, which belong to the model, not the API path — unchunked oversized documents fail synchronously too.


Question 6.7 · Multiple choice · select ONE · Domain 2
A single analyze_document tool handles extraction, summarization, and claim verification, chosen by a mode parameter. The agent regularly picks the wrong mode and results are inconsistent. What is the recommended redesign?
A. Add a fourth mode that automatically detects the right mode
B. Document the modes more thoroughly inside the one description
C. Reduce to two modes by merging extraction into summarization
D. Split the generic tool into purpose-specific tools — extract_data_points, summarize_content, verify_claim_against_source — each with a defined input/output contract

## 6.7
Correct: D
Purpose-specific tools turn a hidden mode decision into a visible selection decision — the thing tool descriptions are good at guiding. Each tool's contract is explicit, and misrouting drops accordingly.
Why not the others: A buries the selection problem one layer deeper; B improves documentation of a structure that remains ambiguous; C reduces options while keeping the overloaded design.


Question 6.8 · Multiple choice · select ONE · Domain 2
When your MCP extraction tool hits a parsing failure, it returns the message “Error: could not parse document” as an ordinary successful text result. The agent then treats that sentence as document content. What is the correct MCP pattern?
A. Prefix error text with “SYSTEM ERROR:” so the agent notices
B. Return the failure with the MCP isError flag set, so the agent programmatically recognizes a tool failure instead of interpreting error prose as data
C. Return an empty string on failure
D. Throw an unhandled exception and let the connection drop



## 6.8
Correct: B
isError is MCP's channel for communicating tool failure: it makes the error a machine-recognizable condition the agent can reason about, rather than text masquerading as a successful result.
Why not the others: A still relies on the model inferring failure from prose conventions; C replaces a mislabeled failure with a silent one; D turns a recoverable tool error into a transport-level breakdown.



Question 6.9 · Multiple response · select TWO · Domain 5
Your extraction system reports 97% aggregate accuracy, and leadership wants to cut human review of high-confidence extractions. Which TWO practices must precede that decision? (Select TWO.)
A. Segment accuracy by document type and field — verifying consistent performance across all segments, since aggregate metrics can mask systematic failures on specific types
B. Accept the 97% aggregate as sufficient evidence on its own
C. Implement stratified random sampling of high-confidence extractions for ongoing error-rate measurement and detection of novel error patterns
D. Stop measuring once review is reduced, to save cost
E. Review only extractions the model itself flags as uncertain




## 6.9
Correct: A, C
Two safeguards make automation defensible: segmentation proves the average isn't hiding a failing document type or field, and stratified sampling of the “safe” population keeps measuring after the humans step back — catching drift and novel errors.
Why not the others: B trusts exactly the number that masks segment failures; D removes the instrumentation precisely when risk increases; E trusts self-flagged uncertainty, which misses the errors the model is confidently wrong about.

Question 6.10 · Multiple response · select TWO · Domain 5
Reviewer capacity covers only a fraction of extractions, so review attention must be routed where errors are likeliest. Which TWO practices form a sound routing design? (Select TWO.)
A. Trust the model's raw self-reported confidence scores without validation
B. Have the model output field-level confidence scores, then calibrate review thresholds against a labeled validation set
C. Review a fixed 1% of extractions chosen by submission order
D. Route to human review the extractions with low calibrated confidence or ambiguous/contradictory source documents, prioritizing limited reviewer capacity where errors concentrate
E. Review only documents longer than ten pages CCAR-



## 6.10
Correct: B, D
Calibration then routing: field-level confidence scores become meaningful once thresholds are tuned on labeled data, and review capacity flows to the calibrated-low-confidence and ambiguous-source cases where errors actually cluster.