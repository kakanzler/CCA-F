"""``api.example`` の非同期 API のテスト。"""

from collections.abc import Iterator
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from api.example import _ITEMS, app


@pytest.fixture
def client() -> Iterator[TestClient]:
    """空のストアを持つテスト用クライアントを返す。

    Yields:
        ``app`` に接続された TestClient。
    """
    _ITEMS.clear()
    with TestClient(app) as test_client:
        yield test_client


def test_create_item_returns_created_item(client: TestClient) -> None:
    """POST /items が 201 と生成済み ID 付きのアイテムを返すこと。"""
    # Arrange
    payload = {"name": "apple", "price": 120.0}

    # Act
    with patch("api.example.generate_item_id", return_value="fixed-id"):
        response = client.post("/items", json=payload)

    # Assert
    assert response.status_code == 201
    assert response.json() == {"id": "fixed-id", "name": "apple", "price": 120.0}


def test_read_item_returns_stored_item(client: TestClient) -> None:
    """GET /items/{item_id} が保存済みのアイテムを返すこと。"""
    # Arrange
    with patch("api.example.generate_item_id", return_value="fixed-id"):
        client.post("/items", json={"name": "banana", "price": 80.0})

    # Act
    response = client.get("/items/fixed-id")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"id": "fixed-id", "name": "banana", "price": 80.0}


def test_read_item_returns_404_for_unknown_id(client: TestClient) -> None:
    """存在しない ID では HTTPException による 404 が返ること。"""
    # Arrange
    unknown_id = "no-such-id"

    # Act
    response = client.get(f"/items/{unknown_id}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == f"item not found: {unknown_id}"


def test_create_item_rejects_negative_price(client: TestClient) -> None:
    """Pydantic の検証により負の価格が 422 で拒否されること。"""
    # Arrange
    payload = {"name": "cherry", "price": -1.0}

    # Act
    response = client.post("/items", json=payload)

    # Assert
    assert response.status_code == 422
