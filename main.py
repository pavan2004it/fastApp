from fastapi import FastAPI, Depends
import schemas
import models
import uvicorn

from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


app = FastAPI()

fakeDatabase = {
    1: {'task': 'Clean car'},
    2: {'task': 'Write blog'},
    3: {'task': 'Start stream'},
}


@app.get("/")
def get_items(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items


@app.get("/{obj_id}")
def get_item(obj_id: int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(obj_id)
    return item


@app.post("/")
def add_item(item: schemas.Item, session: Session = Depends(get_session)):
    item = models.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)

    return item



@app.put("/{obj_id}")
def update_item(obj_id: int, item: schemas.Item, session: Session = Depends(get_session)):
    item_object = session.query(models.Item).get(obj_id)
    item_object.task = item.task
    session.commit()
    return item_object


@app.delete("/{obj_id}")
def delete_item(obj_id: int, session: Session = Depends(get_session)):
    item_object = session.query(models.Item).get(obj_id)
    session.delete(item_object)
    session.commit()
    session.close()
    return 'Item was deleted...'


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)