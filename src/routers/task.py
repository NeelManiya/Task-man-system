from database.database import get_db
from fastapi import APIRouter, HTTPException, Header, Depends, Query
from src.schemas.task import Create_Task_Schema, Get_Tasks_Schema, Update_Task_Schema
from src.utils.user import decode_token
from src.models.task import Task
import uuid
from sqlalchemy.orm import Session
from fastapi_pagination import paginate, Page
from sqlalchemy import select, func

task_router = APIRouter()


@task_router.post("/Create_task")
def create_task(
    task: Create_Task_Schema, token: str = Header(...), db: Session = Depends(get_db)
):
    task_detail = decode_token(token)
    owner_id, email = task_detail

    new_task = Task(
        id=str(uuid.uuid4()),
        title=task.title,
        description=task.description,
        owner_id=owner_id,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return "Task added successfully", new_task


@task_router.get("/Get_task", response_model=list[Get_Tasks_Schema])
def get_task(token: str = Header(...), db: Session = Depends(get_db)):
    task_detail = decode_token(token)
    id, email = task_detail
    find_task = db.query(Task).filter(Task.owner_id == id).all()

    if not find_task:
        raise HTTPException(status_code=400, detail="task not found")

    return find_task


@task_router.patch("/Update_task")
def update_task(id: str, task: Update_Task_Schema, db: Session = Depends(get_db)):
    find_task = db.query(Task).filter(Task.id == id).first()

    if not find_task:
        raise HTTPException(status_code=400, detail="Task not found")

    find_task.title = task.title
    find_task.description = task.description
    find_task.status = task.status

    db.commit()
    db.refresh(find_task)

    return "Task updated successfully", find_task


@task_router.delete("/Delete_task")
def delete_task(id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(status_code=400, detail="Task not found")

    db.delete(task)
    db.commit()

    return "Task deleted successfully"


@task_router.get("/get_all_task")
def get_all_task(db: Session = Depends(get_db)):
    find_task = db.query(Task).all()

    # return find_task
    return {"success": True, "find_task": find_task}


@task_router.get("/get_task")
def get_task(
    db: Session = Depends(get_db),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    total_users = db.execute(select(func.count()).select_from(Task)).scalar()
    Query = select(Task).limit(limit).offset(offset)
    result = db.execute(Query).scalars().all()
    return {
        "total_records": total_users,
        "limit": limit,
        "offset": offset,
        "users": result,
    }
