# app/service.py
from typing import List
from . import crud, schemas  # crud should provide functions used below

class ItemService:
    def __init__(self, db):
        self.db = db

    def create_item(self, item: schemas.ItemCreate):
        # validate or transform as needed, then call crud
        return crud.create_item(self.db, item)

    def get_item(self, item_id: int):
        return crud.get_item(self.db, item_id)

    def list_items(self, skip: int = 0, limit: int = 100) -> List:
        return crud.list_items(self.db, skip=skip, limit=limit)

    def update_item(self, item_id: int, item: schemas.ItemCreate):
        return crud.update_item(self.db, item_id, item)

    def delete_item(self, item_id: int) -> bool:
        return crud.delete_item(self.db, item_id)
