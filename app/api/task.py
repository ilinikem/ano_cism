from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.task import cancel_task, create_task, get_task, task_list
from app.database import get_db
from app.models.task import TaskStatus
from app.schemas.task import TaskCreate, TaskOutDB

router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"]
)


@router.post("/", response_model=TaskOutDB)
async def create(
        task: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await create_task(db, task)


@router.get("/", response_model=List[TaskOutDB])
async def get_task_list(
        status: TaskStatus | None = None,
        limit: int = Query(10, le=100),
        offset: int = 0,
        db: AsyncSession = Depends(get_db)):
    return await task_list(db, status, limit, offset)


@router.get("/{task_id}", response_model=TaskOutDB)
async def get_task_detail(
        task_id: int,
        db: AsyncSession = Depends(get_db)):
    task = await get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/{task_id}/status", response_model=TaskOutDB)
async def get_task_status(
        task_id: int, db: AsyncSession = Depends(get_db)):
    task = await get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "id": task.id,
        "status": task.status
    }


@router.delete("/{task_id}", response_model=TaskOutDB)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    return await cancel_task(db, task_id)
