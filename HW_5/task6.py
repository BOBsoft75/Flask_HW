from pathlib import Path
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, SecretStr
from starlette.responses import RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

USERS = []


class User(BaseModel):
    id_: int
    name: str
    email: EmailStr
    password: SecretStr


USERS.append(User(id_=1, name='user_1',
             email='user_1@example.com', password='112233'))
USERS.append(User(id_=2, name='user_2',
             email='user_2@example.com', password='445566'))
USERS.append(User(id_=3, name='user_3',
             email='user_3@example.com', password='778899'))


@app.get('/', response_class=HTMLResponse)
async def users(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "users": USERS})


@app.post('/user/add')
async def add_user(id_=Form(), name=Form(), email=Form(), password=Form()):
    # USERS.append(User(id_=len(USERS)+1, name=name, email=email, password=password))
    USERS.append(User(id_=id_, name=name, email=email, password=password))
    return RedirectResponse(url='/users/', status_code=302)


if __name__ == "__main__":
    uvicorn.run(f"{Path(__file__).stem}:app", port=8002)
