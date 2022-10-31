from sqlalchemy.orm import Session
from .. import models, schemas


def get_all(db: Session):
    return db.query(models.Item).all()


def get_by_id(id: int, db: Session):
    return db.query(models.Item).filter(models.Item.id == id)


def create(item: schemas.Item, db: Session):
    new_item = models.Item(dec_no=item.dec_no, title=item.title,  user_id=item.user_id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def update(id: int, new_item: schemas.Item, db: Session):
    item = get_by_id(id, db)
    if item.first():
        item.update(new_item.dict())
        db.commit()
        return True

def delete(id: int, db: Session):
    get_by_id(id, db).delete(synchronize_session=False)
    db.commit()