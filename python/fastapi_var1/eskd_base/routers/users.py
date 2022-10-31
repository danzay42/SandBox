from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database
from ..repository import users



router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(item: schemas.Item, db: Session = Depends(database.get_db)):
    return users.create(item, db)


@router.get("/", response_model=list[schemas.ShowUser])
def all(db: Session = Depends(database.get_db)):
    return users.get_all(db)


@router.get("/{id}", response_model=schemas.ShowUser)
def get(id: int, db: Session = Depends(database.get_db)):
    item = users.get_by_id(id, db).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id=} not found")
    return item


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, item: schemas.Item, db: Session = Depends(database.get_db)):
    if users.update(id, item, db):
        return "updated"
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id=} not found")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(database.get_db)):
    users.delete(id, db)
    return "deleted"