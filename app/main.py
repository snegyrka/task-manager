from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import datetime
from app.database import engine, get_db, Base
from app import schemas, crud, auth, business_logic, models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="REST-сервис для управления проектами и задачами",
    version="2.0.0",
)


@app.post("/register", response_model=schemas.UserResponse, tags=["Аутентификация"])
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Регистрация нового пользователя."""
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Имя пользователя уже занято")
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email уже используется")
    return crud.create_user(db, user)


@app.post("/token", response_model=schemas.Token, tags=["Аутентификация"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Вход в систему и получение JWT-токена."""
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/users/me", response_model=schemas.UserResponse, tags=["Пользователи"])
def read_current_user(current_user: models.User = Depends(auth.get_current_user)):
    """Профиль текущего пользователя."""
    return current_user


@app.post("/projects/", response_model=schemas.ProjectResponse, tags=["Проекты"])
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Создать новый проект."""
    return crud.create_project(db, project, current_user.id)


@app.get("/projects/", response_model=list[schemas.ProjectResponse], tags=["Проекты"])
def read_projects(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Список всех проектов."""
    return crud.get_projects(db, current_user.id)


@app.get("/projects/{project_id}", response_model=schemas.ProjectResponse, tags=["Проекты"])
def read_project(project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Получить проект по ID."""
    p = crud.get_project(db, project_id)
    if not p or p.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return p


@app.put("/projects/{project_id}", response_model=schemas.ProjectResponse, tags=["Проекты"])
def update_project(project_id: int, data: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Обновить проект."""
    p = crud.get_project(db, project_id)
    if not p or p.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return crud.update_project(db, project_id, data)


@app.delete("/projects/{project_id}", tags=["Проекты"])
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Удалить проект."""
    p = crud.get_project(db, project_id)
    if not p or p.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Проект не найден")
    crud.delete_project(db, project_id)
    return {"message": "Проект удалён"}


@app.post("/tasks/", response_model=schemas.TaskResponse, tags=["Задачи"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Создать новую задачу."""
    p = crud.get_project(db, task.project_id)
    if not p or p.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return crud.create_task(db, task)


@app.get("/tasks/{project_id}", response_model=list[schemas.TaskResponse], tags=["Задачи"])
def read_tasks(project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Список задач проекта."""
    p = crud.get_project(db, project_id)
    if not p or p.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return crud.get_tasks(db, project_id)


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Задачи"])
def update_task(task_id: int, data: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Обновить задачу."""
    t = crud.get_task(db, task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    p = crud.get_project(db, t.project_id)
    if not p or p.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа")
    return crud.update_task(db, task_id, data.model_dump(exclude_unset=True))


@app.delete("/tasks/{task_id}", tags=["Задачи"])
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Удалить задачу."""
    t = crud.get_task(db, task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    p = crud.get_project(db, t.project_id)
    if not p or p.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа")
    crud.delete_task(db, task_id)
    return {"message": "Задача удалена"}


@app.get("/workload/{project_id}", response_model=list[schemas.WorkloadResponse], tags=["Бизнес-логика"])
def get_workload(project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Загрузка исполнителей проекта."""
    p = crud.get_project(db, project_id)
    if not p or p.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return business_logic.calculate_workload(db, project_id)


@app.get("/suggest-assignee/{project_id}", tags=["Бизнес-логика"])
def suggest_assignee(project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Алгоритм подбора оптимального исполнителя."""
    p = crud.get_project(db, project_id)
    if not p or p.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return business_logic.suggest_task_assignment(db, project_id)


@app.post("/tasks/{task_id}/notify", tags=["Уведомления"])
def notify_assignee(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Отправить уведомление исполнителю."""
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    if not task.assignee_id:
        raise HTTPException(status_code=400, detail="У задачи нет исполнителя")
    project = crud.get_project(db, task.project_id)
    assignee = crud.get_user_by_id(db, task.assignee_id)
    from app.notifications import send_task_assignment_email
    send_task_assignment_email(assignee.email, task.title, project.name)
    return {"message": f"Уведомление отправлено пользователю {assignee.username}"}


@app.get("/deadlines/approaching", response_model=list[schemas.DeadlineTask], tags=["Дедлайны"])
def approaching_deadlines(days_threshold: int = 3, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Задачи с приближающимся дедлайном."""
    tasks = db.query(models.Task).filter(
        models.Task.assignee_id == current_user.id,
        models.Task.status != models.TaskStatus.DONE
    ).all()
    result = []
    limit = datetime.datetime.utcnow() + datetime.timedelta(days=days_threshold)
    for t in tasks:
        if t.deadline and t.deadline <= limit:
            days = (t.deadline - datetime.datetime.utcnow()).days
            result.append({
                "task_id": t.id,
                "title": t.title,
                "days_until_deadline": max(0, days)
            })
    return result