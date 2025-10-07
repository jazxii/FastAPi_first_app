from fastapi import FastAPI, APIRouter, HTTPException
from config import collection
from Database.schemas import all_tasks
from Database.models import Todo, TodoUpdate
from bson import ObjectId
from datetime import datetime

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

@router.put("/{task_id}")
async def update_task(task_id: str, task_update: TodoUpdate):
    try:
        # Validate that task_id is a valid ObjectId
        if not ObjectId.is_valid(task_id):
            raise HTTPException(status_code=400, detail="Invalid task ID format")
        
        # Create update dictionary with only provided fields
        update_data = {}
        if task_update.title is not None:
            update_data["title"] = task_update.title
        if task_update.description is not None:
            update_data["description"] = task_update.description
        if task_update.is_completed is not None:
            update_data["is_completed"] = task_update.is_completed
        if task_update.is_deleted is not None:
            update_data["is_deleted"] = task_update.is_deleted
        
        # Add update timestamp
        update_data["update"] = int(datetime.timestamp(datetime.now()))
        
        # Check if there's anything to update
        if not update_data or len(update_data) == 1:  # Only timestamp
            raise HTTPException(status_code=400, detail="No fields provided for update")
        
        # Find and update the task
        result = collection.update_one(
            {"_id": ObjectId(task_id)}, 
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return {
            "status_code": 200, 
            "message": "Task updated successfully",
            "modified_count": result.modified_count
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong {e}")
 

app.include_router(router)

