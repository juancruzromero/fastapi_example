""" Routes definition"""

from fastapi import APIRouter
from config.db import conn
from models.user import users
from schemas.user import User

from cryptography.fernet import Fernet

# Password cryptography
key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()

@user.get("/users")
def get_users():
    return conn.execute(users.select()).fetchall()

@user.post("/users")
def create_users(user: User):
    new_user = {"name":user.name, "email":user.email}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    #Insert:
    result = conn.execute(users.insert().values(new_user))
    # select * from user where id = "lastrowid"
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()

@user.get("/users/{id}")
def get_user(id:str):
    print(id) # Requst arguments
    return conn.execute(users.select().where(users.c.id == id)).first()

@user.delete("/users/{id}")
def delete_user(id:str):
    print(id) # Requst arguments
    result = conn.execute(users.delete().where(users.c.id == id))
    return f"id {id} deleted"

@user.put("/users/{id}")
def update_user(id: str, user: User):
    conn.execute(users.update().values(name=user.name,
                email=user.email,
                password=f.encrypt(user.password.encode("utf-8"))
    ).where(users.c.id == id))
    return conn.execute(users.select().where(users.c.id == id)).first()

