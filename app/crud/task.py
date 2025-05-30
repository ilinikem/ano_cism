from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate
from app.send_task import send_task_to_queue


async def create_task(db: AsyncSession, task: TaskCreate) -> Task:
    """Создание задачи."""
    task = Task(**task.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    # В очередь RabbitMQ для запуска
    await send_task_to_queue(task.id)
    return task


async def get_task(db: AsyncSession, task_id: int) -> Task | None:
    """Получение задачи по id."""
    res = await db.execute(select(Task).where(Task.id == task_id))
    return res.scalar_one_or_none()


async def cancel_task(db: AsyncSession, task_id: int) -> Task:
    """Отмена задачи по id."""
    task = await get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=404, detail="Task not found")
    if task.status in (
            TaskStatus.COMPLETED,
            TaskStatus.FAILED,
            TaskStatus.CANCELLED):
        raise HTTPException(
            status_code=400, detail="Can't cancel task")

    task.status = TaskStatus.CANCELLED
    task.finished_at = datetime.now(UTC)
    await db.commit()
    await db.refresh(task)
    return task


async def task_list(db: AsyncSession, status: TaskStatus | None,
                    limit: int, offset: int) -> list[Task]:
    """Список задач с фильтрацией и пагинацией."""
    stmt = select(Task)
    if status:
        stmt = stmt.where(Task.status == status)
    stmt = stmt.limit(limit).offset(offset)
    result = await db.execute(stmt)
    return result.scalars().all()
