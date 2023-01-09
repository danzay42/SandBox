from fastapi import APIRouter, Depends, HTTPException, status
from .depends import ItemsRepository, get_user_repository, get_currnet_user, get_item_repository
from models.item import Item, ItemIn, ItemOut
from models.user import User


router = APIRouter()


@router.get("/", response_model=list[ItemOut])
async def all(
    limit: int = 10,
    skip: int = 0,
    items: ItemsRepository = Depends(get_item_repository)
):
    return await items.read(limit=limit, skip=skip)


@router.post("/", response_model=ItemOut)
async def create(
    item: ItemIn,
    items: ItemsRepository = Depends(get_item_repository),
    current_user: User = Depends(get_currnet_user)
):
    return await items.create(item, current_user.id)


@router.put("/", response_model=ItemOut)
async def update(
    id: int,
    item_data: ItemIn,
    items: ItemsRepository = Depends(get_item_repository),
    current_user: User = Depends(get_currnet_user)
):
    item = await items.get_by_id(id)
    if items and current_user.id == item.user:
        return await items.update(id, item_data, item.user)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")


@router.delete("/")
async def delete(
    id: int,
    items: ItemsRepository = Depends(get_item_repository),
    current_user: User = Depends(get_currnet_user)
):

    if current_user.id == id:
        return await items.delete(id)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")

