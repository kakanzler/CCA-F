"""数値データの集計ユーティリティ。"""


def summarize(values: list[float]) -> dict[str, float]:
    """数値リストの統計サマリを返す。

    Args:
        values: 集計対象の数値リスト。

    Returns:
        以下のキーを持つ辞書。

        - ``count``: 要素数。
        - ``sum``: 合計値。
        - ``mean``: 平均値。
        - ``min``: 最小値。
        - ``max``: 最大値。

    Raises:
        ValueError: values が空の場合。

    Examples:
        >>> summarize([1.0, 2.0, 3.0])
        {'count': 3, 'sum': 6.0, 'mean': 2.0, 'min': 1.0, 'max': 3.0}
    """
    if not values:
        raise ValueError("values must not be empty")

    total = float(sum(values))
    return {
        "count": len(values),
        "sum": total,
        "mean": total / len(values),
        "min": float(min(values)),
        "max": float(max(values)),
    }
