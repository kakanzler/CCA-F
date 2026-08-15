# 02---Building_with_the_Claude_API

Anthropic Academy「Building with the Claude API」の作業ディレクトリ。

## 環境構築

Python は **3.14.5（正式版）** を使う。

> ⚠️ **素の `python` を使わないこと。**
> このマシンでは `python` が pyenv shim 経由で **3.14.0a5（アルファ版）** に解決される。
> アルファ版は C-ABI が正式版と非互換で、`import anthropic` が
> アクセス違反 (0xC0000005) でクラッシュする。
> venv を作るときは必ずインタプリタを絶対パスで指定する。

### 1. venv を作る

```powershell
cd reference\02---Building_with_the_Claude_API
& "$env:APPDATA\uv\python\cpython-3.14-windows-x86_64-none\python.exe" -m venv .venv
```

### 2. 有効化する

```powershell
.venv\Scripts\Activate.ps1
```

> PowerShell では `.venv\Scripts\activate` ではなく **`Activate.ps1`**。
> 前者は activate.bat が別プロセスで走るだけで、有効化が残らない。

有効化されたか確認:

```powershell
python --version   # Python 3.14.5 と出ること（a5 ではない）
```

### 3. パッケージを入れる

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

初回に requirements.txt を作ったときのコマンドは以下。

```powershell
pip install anthropic python-dotenv jupyter
pip freeze > requirements.txt
```

### 4. API キーを置く

このディレクトリ直下に `.env` を作り、Anthropic Console で発行したキーを書く。

```
ANTHROPIC_API_KEY=sk-ant-...
```

`.env` はリポジトリルートの `.gitignore` で全階層無視されるのでコミットされない。

Notebook 側からはこう読む:

```python
from dotenv import load_dotenv
load_dotenv()          # .env を環境変数に読み込む

from anthropic import Anthropic
client = Anthropic()   # ANTHROPIC_API_KEY を自動で拾う
```

### 5. Notebook のカーネルを .venv に向ける

> ⚠️ **この `.venv` は VSCode に自動検出されない。**
> Python 拡張が自動で拾うのは**ワークスペース直下**の `.venv` だけ。
> このリポジトリではワークスペースルートが `402---CCA-F` で、
> venv は 2 階層下の `reference/02---Building_with_the_Claude_API/.venv` にあるため
> 検出対象外になる。下記のとおりカーネルを明示登録する。

#### 5-1. カーネルを登録する（初回のみ）

```powershell
.venv\Scripts\python.exe -m ipykernel install --user --name cca-02-claude-api --display-name "Python 3.14.5 (02 Claude API .venv)"
```

`%APPDATA%\jupyter\kernels\cca-02-claude-api\` に登録される。
表示名を付けておくことで、後述のバージョン表示の重複問題も回避できる。

#### 5-2. カーネルを選ぶ

1. `Ctrl+Shift+P` → `Developer: Reload Window`
   （登録直後は再読み込みしないと Jupyter 拡張が拾わない）
2. Notebook 右上の **カーネルの選択** → **`Jupyter Kernel...`**
   （`Python Environments...` ではない）
3. **`Python 3.14.5 (02 Claude API .venv)`** を選ぶ

> ⚠️ **バージョン表示だけで選ばないこと。**
> この venv のベースは uv 管理の Python なので、
> グローバル側も `.venv` も **どちらも `Python 3.14.5` と表示される**。
> 5-1 で付けた表示名か、パスで判別する。

#### 「requires the ipykernel package」と出たら

グローバル側を掴んでいる。**「Install」を押さないこと**
（グローバル環境に ipykernel が入り、venv で分離した意味がなくなる）。
**「Change Kernel」** を押して上記のカーネルを選び直す。

#### カーネルの確認方法

セルで以下を実行する。

```python
import sys
print(sys.executable)
```

`...\02---Building_with_the_Claude_API\.venv\Scripts\python.exe` と出れば正しい。

`!python --version` ではシェルの PATH を見てしまい、カーネルの確認にならない
（pyenv shim 経由でアルファ版を拾うことすらある）。必ず `sys.executable` で確認する。

## Note

- pip のバージョンが古い時は Update すること
    ```powershell
    python -m pip install --upgrade pip
    ```
- `pyenv update` はこの Windows 11 環境では動かない
  （内部で使う `htmlfile` COM が IE 廃止により利用不可）。
  pyenv 側のバージョンDBは 2025/02 で止まっているため、
  3.14 正式版は pyenv からは入れられない。上記の uv 管理の Python を使っている。
