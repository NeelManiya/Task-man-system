from pydantic import BaseModel


class Create_Task_Schema(BaseModel):
    title: str
    description: str


class Get_Tasks_Schema(BaseModel):
    id: str
    title: str
    description: str
    status: str


class Update_Task_Schema(BaseModel):
    title: str
    description: str
    status: str
