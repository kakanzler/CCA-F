"""テスト共通のセットアップ。"""

import importlib.util
import sys
from pathlib import Path

_MODULE_PATH = Path(__file__).resolve().parent.parent / "src" / "example.text.py"


def _register_example_text() -> None:
    """``src/example.text.py`` を ``example_text`` としてインポート可能にする。

    ファイル名にドットが含まれるため通常の import 文では読み込めない。
    importlib で明示的にロードし、``sys.modules`` に登録する。

    Raises:
        ImportError: モジュール spec の生成に失敗した場合。
    """
    spec = importlib.util.spec_from_file_location("example_text", _MODULE_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load module from {_MODULE_PATH}")

    module = importlib.util.module_from_spec(spec)
    sys.modules["example_text"] = module
    spec.loader.exec_module(module)


_register_example_text()
