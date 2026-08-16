# Exercise 3

   ‐ `exercise3.ipynb`での実行結果から得た学びをまとめる。

## Learning

1. JSON schemaのextraction toolを実装しよう
   - client.messages.create()でmessageをLLMに投げる際にtools=[]にtool_schema(JSON schema)を指定する。
   - 1階層のname, description, input_schemaは必須フィールド。
   - 2階層のinput_schemaの中身は任意で、この中身はLLMにはテキスト情報として扱われる。そのため、フィールド名に誤記があっても処理は通るが、正しく解釈させるためにはtype, required,description など慣習に見られるものを使うべきで、何でもかんでも使えばいいというものではない。
     - またテキスト情報を構造化して渡すだけだからここでの定義は必ず守られることを保証しない。
   - client.messages.create()のtool_choiceはデフォルト{"type" : "auto"}でClaudeがすべて判断するモードになっているが、ここで{"type": "tool" , "name", "xxx"}でToolを使う際は必ずxxxというToolを使うように制御できる。ほかにも{"type": "any"}で必ず何かしらのToolを使うよう制御できる。
     - auto（テキストで答えてもよい）／any（何かのツールは必須、選択はモデル任せ）／特定ツール指定（必ずそのツールを使う）。文書種類が不明で複数抽出スキーマがある場合に any を使う
2. validation-retry loopを実装しよう
   - pydanticを使う場合、pydantic.BaseModelを継承して新しい型定義を実装できる。この型を用いることで同時に検証も行われる。また、@model_validatorで型定義のみで表現できない細かい設定を定義できる。(関数名は何でもよい) またmode="after"をデコレータの引数に指定すると、型定義のチェック後にValidateが行われるので型が通ることを前提にチェックできる。
   - try ~ exceptで pydantic.ValidationErrorをキャッチすることでBaseModelでのエラーをキャッチできる。
   - retry処理とは、このLLMからのQueryのResponseをこのBaseModelで定義した新しい型をチェックし、意図にそぐわない場合に、Response(Assistant)と型検証失敗(user)をmessageにして再度queryを投げる処理を指す。
3. few-shot examplesを実装しよう
   - promptに<input example>/<ideal output>を埋め込むことで、
     モデルの出力傾向を誘導できる（例：情報が無い項目でnullを返す挙動の強化）。
   - ただし2で作ったretry loop（is_error=Trueのtool_result）自体もモデルへの
     フィードバックとして機能するため、few-shotとretry loopは別の仕組みである
     ことに注意。retryは「検証失敗時に事後的に例を1件与える」ことに近い。

4. batch processing strategyを設計しよう（実装はせず設計に留めた）
   - custom_idは意味のある文字列にし、投入したテキストとの対応表を
     こちら側で保持する（バッチAPIは失敗後に元の入力内容を返さないため）。
   - 結果のresult.typeで分岐:
     - succeeded → 3のvalidationを通し、失敗すれば5の人間レビューへ
     - errored → 原因を見て、コンテキスト長超過ならチャンク分割して再投入、
       一時的障害ならそのまま再投入
     - expired → そのまま再投入
   - SLA設計: Batch最悪処理時間24hに対し、SLAが30hなら後処理時間を見込んで
     間隔を6h未満、例えば4hに設定する（間隔+24h+後処理 ≤ SLA）。

5. 人間によるreview戦略を実装しよう
   - 3の実験で判明: ValidationErrorをそのままretryに回すと、モデルは元データを
     読み直すのではなく、検証を通すために実態と異なる値ででっち上げることがある
     （例: 保守費30,000円を40,000円に書き換えて合計を辻褄合わせ）。
   - そのため、confidence scoreのような曖昧な基準ではなく、
     「算術的整合性など特定のvalidatorが失敗した場合は即座に人間レビューへ回し、
     形式ずれなど直る見込みのあるエラーのみretryする」という、
     エラー種別に基づく分岐が実務的な設計となる。


## summary

3行まとめ
・JSON SchemaでLLMは構造的に情報を理解することができるが、必ず記載の通りになるという強制力はない。その強制力があるのは正しく書かれたスキーマ(型・enum・required)限定で、フィールド名の誤記など不正なキーは無視されて素通りする。
・Pydanticにより型を新規に定義(BaseModel、model_validator)することで検証も可能。またValidationErrorを用いれば検証時のエラーハンドリングが可能だが、そのまま投げ返すとLLMは帳尻を合わせるために実体と異なる情報で埋める可能性があるため、人がReviewするプロセスを作るのが望ましい場合がある。
・Batch処理はexpiredやAPIエラーの場合はそのまま再投入するが、context超過などの場合はチャンクに分けて再投入する必要がある。また、再投入にあたり、意味のある名前で命名したcustom_idと投入するテキスト情報を事前に紐づけておく必要がある。
