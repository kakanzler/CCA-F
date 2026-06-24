# commit-refined-summary

`/refine-summary` 実行後、手動で修正した summary.md / origin.md をコミットしてプッシュするコマンド。直前に編集していたモジュールのフォルダ **のみ** を対象にする。

## Steps

1. IDEで開いているファイルのディレクトリを特定する。開いているファイルが summary.md でも origin.md でもない場合はその旨を伝えて終了する。

2. 対象ディレクトリの origin.md と summary.md の両方が存在することを確認する。どちらかが欠けている場合はその旨を伝えて終了する。

3. 対象ディレクトリのパスから以下を抽出する（`reference/XX---aaaaa/YY_bbbbb/` という構成を前提とする）:
   - `YY` = モジュール番号（例: `07`）
   - `bbbbb` = モジュール名（例: `Code_Review`）。コミットメッセージでは読みやすいよう `_` を空白に置き換える（例: `Code Review`）。

4. 対象ディレクトリの origin.md と summary.md のみをステージする。**他のフォルダの変更や README.md など、対象ディレクトリ外のファイルはステージしない。**
   ```sh
   git add reference/XX---aaaaa/YY_bbbbb/origin.md reference/XX---aaaaa/YY_bbbbb/summary.md
   ```

5. ステージ内容を `git status --short` で確認し、対象ディレクトリの2ファイルだけが含まれていることを検証する。想定外のファイルが含まれていたら中断してユーザーに報告する。

6. 以下の形式でコミットする:
   ```
   docs : add lesson YY (bbbbb) summary and origin
   ```
   ※ 既にコミット済みでファイルに差分がない場合は、その旨を伝えてコミットをスキップする。

7. `git push` でリモートに反映する。

8. コミットハッシュとプッシュ結果を簡潔に報告する。
