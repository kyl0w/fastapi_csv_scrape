from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.responses import RedirectResponse
from .schemas import UserOut, UserAuth, TokenSchema, SystemUser, LoginSchema
from .utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)
from uuid import uuid4
from .deps import get_current_user
from sqlalchemy.orm import Session
from .models import User
from .database import init_db
from .deps import get_db
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from .scrape import process_csv

init_db()

app = FastAPI()

@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')


@app.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    new_user = User(
        email=data.email,
        password=get_hashed_password(data.password),
        id=str(uuid4())
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user) 

    return UserOut(id=new_user.id, email=new_user.email)


@app.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if user is None or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }
    
@app.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: SystemUser = Depends(get_current_user)):
    return user

# Scrape

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), current_user: str = Depends(get_current_user)):
    # Lê o conteúdo do arquivo CSV
    contents = await file.read()
    # Converte o conteúdo em bytes para uma string
    file_content = contents.decode("utf-8").splitlines()
    
    # Processa o CSV e faz o scraping
    results = process_csv(file_content)
    
    return {"user": current_user, "results": results}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    task = tasks_status.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task["status"] == "In Progress" and scrape_urls.AsyncResult(task_id).ready():
        # Atualiza o status quando a tarefa estiver concluída
        task["status"] = "Completed"
        task["result"] = scrape_urls.AsyncResult(task_id).result
    
    return task


@app.get("/results/{task_id}")
async def get_results(task_id: str):
    task = tasks_status.get(task_id)
    if not task or task["status"] != "Completed":
        raise HTTPException(status_code=404, detail="Task not completed yet or task not found")
    
    return task["result"]