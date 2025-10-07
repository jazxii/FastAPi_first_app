from fastapi import FastAPI, APIRouter, HTTPException
from config import collection
from Database.schemas import all_tasks
from Database.models import Todo

app = FastAPI()
router = APIRouter()

# @app.get("/")
# async def homepage():
#     return {"message": "Welcome to the FastAPI application!"}
@router.get("/")
async def get_all_todos():
    data = collection.find( )
    return all_tasks(data)

@router.post("/")
async def create_task(new_task: Todo):
    try:
        resp = collection.insert_one(dict(new_task))
        return {"status_code":200, "id":str(resp.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong {e}")
 

app.include_router(router)

