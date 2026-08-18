from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# ---- Pydantic 模型 ----
# 请求体模型：添加清单项时，客户端只需要传 name（字符串）
class ItemCreate(BaseModel):
    name: str


# 响应体模型：返回给客户端的清单项，包含服务器分配的 id 和 name
class Item(BaseModel):
    id: int
    name: str


# ---- 内存存储 ----
# 用一个 list 存所有清单项，每个元素是一个 Item 实例
items: list[Item] = []
# 简单的自增 id，模拟数据库主键
next_id = 1


# ---- 三个接口 ----

# 1. 添加一个清单项
@app.post("/items", response_model=Item, status_code=201)
def create_item(payload: ItemCreate) -> Item:
    global next_id
    item = Item(id=next_id, name=payload.name)
    next_id += 1
    items.append(item)
    return item


# 2. 列出所有清单项
@app.get("/items", response_model=list[Item])
def list_items() -> list[Item]:
    return items


# 3. 删除一个清单项
@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int) -> Item:
    for item in items:
        if item.id == item_id:
            items.remove(item)
            return item
    # 找不到对应 id 时返回 404
    raise HTTPException(status_code=404, detail="Item not found")