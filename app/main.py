from fastapi import FastAPI

from app.api import task

app = FastAPI(title="Task Service")

app.include_router(task.router)
