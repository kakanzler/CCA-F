"""汎用ユーティリティ関数。"""


def add(a: float, b: float) -> float:
    """2 つの数値を足し合わせる。

    Args:
        a: 加算する 1 つ目の数値。
        b: 加算する 2 つ目の数値。

    Returns:
        a と b の和。

    Raises:
        TypeError: a または b が数値でない場合。

    Examples:
        >>> add(1, 2)
        3
    """
    for name, value in (("a", a), ("b", b)):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(
                f"add() argument '{name}' must be int or float, "
                f"got {type(value).__name__}"
            )

    return a + b
