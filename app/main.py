from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.service import classify_task_priority, completion_percentage

app = FastAPI(
    title="TaskPulse API",
    version="1.0.0",
    description="A small task tracking API used for realistic CI/CD validation.",
)


class TaskStatusRequest(BaseModel):
    task_name: str = Field(min_length=1)
    completed_steps: int = Field(ge=0)
    total_steps: int = Field(gt=0)
    open_dependencies: int = Field(ge=0)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "taskpulse-api"}


@app.post("/task/status")
def task_status(payload: TaskStatusRequest) -> dict:
    return {
        "task_name": payload.task_name,
        "completion_percentage": completion_percentage(
            payload.completed_steps,
            payload.total_steps,
        ),
        "priority": classify_task_priority(payload.open_dependencies),
    }
