import platform
import uvicorn
from topics_practices.database_connection.sqlite.models import model, schema
from topics_practices.database_connection.db_connect import engine
from util import get_db
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session


model.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Hello World')


@app.get('/')
def home():
    return {
        "message": "hello"
    }


@app.post('/post')
def createPost(request: schema.Blog, db: Session = Depends(get_db)):
    new_blog = model.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data_recieved": new_blog}


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2)


if __name__ == "__main__":
    if platform.system() == "Windows":
        main()
