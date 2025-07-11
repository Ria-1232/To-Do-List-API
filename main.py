from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Todo
from database import SessionLocal, engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="📝 To-Do List API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes

@app.get("/")
def root():
    return {"message": "Welcome to the To-Do API!"}

@app.post("/todos/")
def create_task(title: str, description: str = "", db: Session = Depends(get_db)):
    todo = Todo(title=title, description=description)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@app.get("/todos/")
def read_tasks(db: Session = Depends(get_db)):
    return db.query(Todo).all()

@app.get("/todos/{todo_id}")
def read_task(todo_id: int, db: Session = Depends(get_db)):
    task = db.query(Todo).filter(Todo.id == todo_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/todos/{todo_id}")
def update_task(todo_id: int, title: str = None, description: str = None, db: Session = Depends(get_db)):
    task = db.query(Todo).filter(Todo.id == todo_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if title:
        task.title = title
    if description:
        task.description = description
    db.commit()
    return task

@app.delete("/todos/{todo_id}")
def delete_task(todo_id: int, db: Session = Depends(get_db)):
    task = db.query(Todo).filter(Todo.id == todo_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
