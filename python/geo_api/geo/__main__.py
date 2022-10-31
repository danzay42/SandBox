from fastapi import FastAPI
from geo.db import init_db, init_name_support
from geo.repository import timezone_diff

app = FastAPI(title="GeoNames API")
db: dict
db_names: dict

@app.on_event("startup")
def db_up():
    global db, db_names
    print("Create DB")
    db = init_db("RU.txt")
    db_names = init_name_support(db)
    print(f"{len(db)=}, {len(db_names)=}")

@app.get('/info')
async def info(id: int):
    return db.get(id)

@app.get('/')
async def pagination(page: int = 0, limit: int = 10):
    skip = page*limit
    return list(db.values())[skip:skip+limit]

@app.get('/diff')
async def diff(name_1: str, name_2: str):
    t1 = db.get(db_names[name_1][0])
    t2 = db.get(db_names[name_2][0])

    if not (t1 and t2):
        return None
    
    res = {}
    res[name_1] = t1
    res[name_2] = t2
    res["north"] = name_1 if float(t1["latitude"]) >= float(t2["latitude"]) else name_2
    time_delta, time_delta_str = timezone_diff(t1["timezone"], t2["timezone"])
    res["is_same_time"] = time_delta == 0
    res["timezone_diff"] = time_delta_str 

    return res

@app.get('/help')
async def help(name_part: str, limit: int = 10):
    return [name for name in db_names.keys() if name.startswith(name_part)][:limit]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("geo.__main__:app", port=8000, host="127.0.0.1", reload=True)
