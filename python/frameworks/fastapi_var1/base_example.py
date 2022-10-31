from fastapi import FastAPI

db = {i: {"id": i, "title": f"object {i}"} for i in range(100)}
router = FastAPI()

@router.post("/items")
def create(id: int, title: None | str = "test object"):
    if id in db.keys():
        return f"{id} is busy!"    
    else:
        db[id] = {"id": id, "title": title}
        return f"{title} with {id} created!"
        
@router.get("/items")
def list(skip:int=10, limit:int=50):
    return [item for item in db.values()][skip:skip+limit]

@router.get("/items/{id}")
def item(id:int):
    return db[id]

@router.put("/items/{id}")
def update(id: int, title: None | str = "updated title"):
    db[id]['title'] = title
    return db[id]

@router.delete("/items/{id}")
def delete(id: int):
    if id in db.keys():
        item = db.pop(id)
        return f"{item['title']} with {id} deleted!"  
    else:
        return f"{id} is deleted already!"  
