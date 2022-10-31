from fastapi import APIRouter, Depends, HTTPException, status
from .depends import UserRepository, get_user_repository, get_currnet_user
from models.user import User, UserIn, UserOut


router = APIRouter()


@router.get("/", response_model=list[User])
async def all(
    limit: int = 10,
    skip: int = 0,
    users: UserRepository = Depends(get_user_repository)):
    return await users.get_all(limit=limit, skip=skip)


@router.post("/", response_model=UserOut)
async def create(
    user: UserIn,
    users: UserRepository = Depends(get_user_repository)):
    return await users.create(user)


@router.put("/", response_model=UserOut)
async def update(
    id: int,
    user_data: UserIn,
    users: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_currnet_user)):

    user = await users.get_by_id(id=id)
    if user and current_user.email == user.email:
        return await users.update(id, user_data)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")