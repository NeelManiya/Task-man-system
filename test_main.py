from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


# task.py api
def test_read_main():
    response = client.get("/get_all_task")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] and "find_task" in data
