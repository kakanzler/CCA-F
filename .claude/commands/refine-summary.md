# refine-summary

Anthropic Academyのまとめ作業用コマンド。現在開いているsummary.mdをorigin.mdと照合してrefineし、理解度を評価する。

## Steps

1. IDEで開いているファイルのディレクトリを特定する。開いているファイルがsummary.mdでない場合はその旨を伝えて終了する。

2. 同じディレクトリにあるorigin.mdを読む。

3. summary.mdを読む。

4. origin.mdと比較して、summary.mdに以下の観点でrefineを行う:
   - 抜けている重要な概念・機能
   - 不正確または不完全な記述
   - origin.mdで強調されているのに未記載の点
   - 既存の記述はできるだけ保持し、追加・修正のみ行う

5. refineしたsummary.mdを保存する。

6. 元のsummary.md（refine前）の内容を基に理解度を評価する:
   - 総合評価（A/B/Cなど）
   - 良かった点（何を正しく理解できていたか）
   - 抜けていた点（何が見落とされていたか、それが概念的な誤解か細部の見落としかも示す）
   - 次回へのアドバイス
