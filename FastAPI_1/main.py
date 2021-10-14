from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel



# API object
app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

# @app.get('/')
# def home():
#     return {"Data": "Test"}
#
#
# @app.get("/about")
# def about():
#     return {"Data": "About"}


inventory = {}


@app.get("/get-item/{item_id}")
# None is a default value
def det_item(item_id: int = Path(None, description="The ID of the item", gt=0)):
    return inventory[item_id]


@app.get("/get-by-name")
def det_item(name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id]["name"].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=404, detail="Item name not found.")


# @app.get("/get-by-name/{item_id}")
# def det_item(item_id: int, name: Optional[str] = None):
#     for item_id in inventory:
#         if inventory[item_id]["name"] == name:
#             return inventory[item_id]
#     return {"Data": "Not found"}

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item ID already exist.")

    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="ID does not exist.")

    if item.name != None:
        inventory[item_id].name = item.name

    if item.price != None:
        inventory[item_id].price = item.price

    if item.brand is not None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]


@app.delete("/delete-ite")
def delete_item(item_id: int = Query(..., description="The ID of the item", gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="ID does not exist.")

    del inventory[item_id]
    return {"Success": "Item deleted!"}


# uvicorn main:app --reload
