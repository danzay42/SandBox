import datetime
from db.items import items
from models.item import Item, ItemIn, ItemOut
from .base import BaseRepository


class ItemsRepository(BaseRepository):

    async def get_by_id(self, id: int) -> Item | None:
        query = items.select().where(items.c.id == id)
        i = await self.database.fetch_one(query=query)
        if i is None:
            return None
        return Item.parse_obj(i)

    async def create(self, i: ItemIn, user_id: int) -> Item:
        item = Item(
            dec_no=i.dec_no,
            user=user_id,
            title=i.title,
            is_bool=i.is_bool,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        values = {**item.dict()}
        values.pop("id", None)

        query = items.insert().values(**values)
        items.id = await self.database.execute(query)
        return item

    async def read(self, limit: int = 100, skip: int = 0) -> list[Item]:
        query = items.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def update(self, id: int, i: ItemIn, user_id: int) -> Item:
        item = Item(
            dec_no=i.dec_no,
            user=user_id,
            title=i.title,
            is_bool=i.is_bool,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        values = {**item.dict()}
        values.pop("id", None)
        values.pop("created_at", None)

        query = items.update().where(items.c.id == id).values(**values)
        await self.database.execute(query)
        return item


    async def delete(self, id: int):
        query = items.delete().where(items.c.id == id)
        await self.database.execute(query=query)
