from sqlalchemy.orm import Session
from .. import models, schemas, hashing


def get_all(db: Session):
    return db.query(models.User).all()


def get_by_id(id: int, db: Session):
    return db.query(models.User).filter(models.User.id == id)


def create(user: schemas.User, db: Session):
    new_user = models.User(name=user.name, email=user.email, password=hashing.Hash.bcrypt(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update(id: int, new_item: schemas.User, db: Session):
    item = get_by_id(id, db)
    if item.first():
        item.update(new_item.dict())
        db.commit()
        return True

def delete(id: int, db: Session):
    get_by_id(id, db).delete(synchronize_session=False)
    db.commit()