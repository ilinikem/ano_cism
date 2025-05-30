import pytest

from app.crud.task import cancel_task, create_task, get_task, task_list
from app.models.task import TaskStatus
from app.schemas.task import TaskCreate


@pytest.mark.asyncio
async def test_create_task(async_session):
    task_data = TaskCreate(
        title="Test task",
        description="Test description",
        priority="MEDIUM"
    )
    task = await create_task(async_session, task_data)
    assert task.id is not None
    assert task.title == "Test task"
    assert task.status == TaskStatus.NEW


@pytest.mark.asyncio
async def test_get_task(async_session):
    task_data = TaskCreate(title="Get task", priority="LOW")
    created_task = await create_task(async_session, task_data)
    fetched_task = await get_task(async_session, created_task.id)
    assert fetched_task.id == created_task.id


@pytest.mark.asyncio
async def test_cancel_task(async_session):
    task_data = TaskCreate(title="Cancel task", priority="HIGH")
    task = await create_task(async_session, task_data)
    cancelled_task = await cancel_task(async_session, task.id)
    assert cancelled_task.status == TaskStatus.CANCELLED


@pytest.mark.asyncio
async def test_task_list(async_session):
    # Несколько задач
    for i in range(5):
        await create_task(async_session, TaskCreate(title=f"Task {i}"))
    tasks = await task_list(async_session, None, limit=5, offset=0)
    assert len(tasks) >= 5
