import asyncio
import os
from datetime import datetime, timezone

from aio_pika import IncomingMessage, connect_robust

from app.database import AsyncSessionLocal
from app.models.task import Task, TaskStatus

RABBIT_HOST = "localhost"
env = os.getenv("ENVIRONMENT", "dev")

if env == "prod":
    RABBIT_HOST = "rabbitmq"

RABBITMQ_URL = f"amqp://guest:guest@{RABBIT_HOST}:5672/"
QUEUE_NAME = "tasks_queue"


async def process_task(task_id: int):
    async with AsyncSessionLocal() as db:
        task = await db.get(Task, task_id)
        if not task:
            print(f"Task {task_id} not found")
            return

        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now(timezone.utc)
        await db.commit()

        print(f"Processing task {task_id}...")
        # Имитация работы
        await asyncio.sleep(15)

        task.status = TaskStatus.COMPLETED
        task.finished_at = datetime.now(timezone.utc)
        task.result = "Задача выполнена"
        await db.commit()

        print(f"Task {task_id} completed.")


async def on_message(message: IncomingMessage):
    async with message.process():
        try:
            task_id = int(message.body.decode())
            await process_task(task_id)
        except Exception as e:
            print(f"Ошибка при обработке сообщения: {e}")


async def main():
    connection = await connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    await queue.consume(on_message)
    print("Worker запущен, ожидает сообщения...")
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
