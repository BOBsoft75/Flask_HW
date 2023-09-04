from pathlib import Path
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, EmailStr, SecretStr

app = FastAPI()


USERS = []


class User(BaseModel):
    id_: int
    name: str
    email: EmailStr
    password: SecretStr


@app.get('/users/')
async def all_users():
    return {'users': USERS}


@app.post('/user/add')
async def add_user(user: User):
    USERS.append(user)
    return {"user": user, "status": "added"}


@app.put('/user/{user_id}')
async def update_user(user_id: int, user: User):
    user_to_update = next((u for u in USERS if u.id_ == user_id), None)
    if user_to_update is None:
        return {"error": "User not found"}

    for field in user.__dict__:
        if field in user_to_update.__dict__:
            user_to_update.__dict__[field] = user.__dict__[field]
    USERS.append(user_to_update)
    return {"user": user_to_update, "status": "updated"}


@app.delete('/user/{user_id}')
async def delete_user(user_id: int):
    user_to_delete = next((u for u in USERS if u.id_ == user_id), None)
    if user_to_delete is None:
        return {"error": "User not found"}

    USERS.remove(user_to_delete)
    return {"status": "deleted"}


if __name__ == "__main__":
    file_name = Path(__file__).stem
    uvicorn.run(f"{file_name}:app", port=8001)