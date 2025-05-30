import os

import aio_pika

RABBIT_HOST = "localhost"
env = os.getenv("ENVIRONMENT", "dev")

if env == "prod":
    RABBIT_HOST = "rabbitmq"

RABBITMQ_URL = f"amqp://guest:guest@{RABBIT_HOST}:5672/"
QUEUE_NAME = "tasks_queue"


async def send_task_to_queue(task_id: int):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=str(task_id).encode()),
            routing_key=QUEUE_NAME,
        )
