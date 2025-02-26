from src.routers.user import user_router
from src.routers.task import task_router
from fastapi import FastAPI
from fastapi_pagination import add_pagination

app = FastAPI()
add_pagination(app)

app.include_router(user_router)
app.include_router(task_router)
