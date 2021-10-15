import fastapi as _fastapi
import services as _services
import schemas as _schemas
import sqlalchemy.orm as _orm
from typing import List


app = _fastapi.FastAPI()

_services.create_database()


@app.post("/users/", response_model=_schemas.User)
def create_user(user: _schemas.UserCreate, db: _orm.Session=_fastapi.Depends(_services.get_bd)):
    db_user = _services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="The email is in use")

    return _services.create_user(db=db, user=user)


@app.get("/users/", response_model=List[_schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_bd)):
    users = _services.get_users(db=db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=_schemas.User)
def read_user(user_id: int, db: _orm.Session = _fastapi.Depends(_services.get_bd)):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(status_code=404, detail="this user does not exist")

    return db_user
