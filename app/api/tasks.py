
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Response, status

from app.models.task import (
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(payload: TaskCreate):
    return task_service.create_task(payload)


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    task_status: Optional[TaskStatus] = Query(default=None, alias="status"),
    priority: Optional[TaskPriority] = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return task_service.list_tasks(
        status=task_status.value if task_status else None,
        priority=priority.value if priority else None,
        limit=limit,
        offset=offset,
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = task_service.get_task(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, payload: TaskUpdate):
    task = task_service.update_task(task_id, payload)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    deleted = task_service.delete_task(task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

