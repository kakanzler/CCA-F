"""FastAPI を用いた非同期サンプル API。"""

from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Example API")


class ItemCreate(BaseModel):
    """アイテム作成リクエストのモデル。

    Attributes:
        name: アイテム名。1 文字以上。
        price: 価格。0 以上。
    """

    name: str = Field(min_length=1)
    price: float = Field(ge=0)


class Item(BaseModel):
    """アイテムのレスポンスモデル。

    Attributes:
        id: アイテムを一意に識別する ID。
        name: アイテム名。
        price: 価格。
    """

    id: str
    name: str
    price: float


_ITEMS: dict[str, Item] = {}


def generate_item_id() -> str:
    """新しいアイテム ID を生成する。

    Returns:
        UUID4 形式の文字列。
    """
    return str(uuid4())


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemCreate) -> Item:
    """アイテムを作成する。

    Args:
        payload: 作成するアイテムの内容。

    Returns:
        生成された ID を含む作成後のアイテム。
    """
    item = Item(id=generate_item_id(), name=payload.name, price=payload.price)
    _ITEMS[item.id] = item
    return item


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str) -> Item:
    """アイテムを 1 件取得する。

    Args:
        item_id: 取得するアイテムの ID。

    Returns:
        該当するアイテム。

    Raises:
        HTTPException: 該当するアイテムが存在しない場合 (404)。
    """
    item = _ITEMS.get(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"item not found: {item_id}",
        )
    return item
