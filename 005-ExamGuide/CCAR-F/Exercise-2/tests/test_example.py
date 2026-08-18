"""``example_text.summarize`` のテスト。"""

import pytest

from example_text import summarize


def test_summarize_returns_all_statistics() -> None:
    """全ての統計値が正しく計算されること。"""
    result = summarize([1.0, 2.0, 3.0, 4.0])

    assert result == {
        "count": 4,
        "sum": 10.0,
        "mean": 2.5,
        "min": 1.0,
        "max": 4.0,
    }


def test_summarize_with_single_value() -> None:
    """要素が 1 つの場合も全ての統計値が同じ値になること。"""
    result = summarize([5.0])

    assert result == {
        "count": 1,
        "sum": 5.0,
        "mean": 5.0,
        "min": 5.0,
        "max": 5.0,
    }


def test_summarize_with_negative_values() -> None:
    """負の数を含む場合も最小値・最大値が正しいこと。"""
    result = summarize([-3.0, 1.0, -7.0])

    assert result["min"] == -7.0
    assert result["max"] == 1.0
    assert result["sum"] == -9.0


def test_summarize_raises_on_empty_list() -> None:
    """空リストを渡すと ValueError が送出されること。"""
    with pytest.raises(ValueError, match="must not be empty"):
        summarize([])
