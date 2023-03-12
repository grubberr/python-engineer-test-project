import jwt
from apiflask import APIBlueprint, HTTPTokenAuth, Schema, abort
from apiflask.fields import String
from flask import current_app

from app.model import User, db

login_api = APIBlueprint("login", __name__)
auth = HTTPTokenAuth()


class LoginIn(Schema):
    email = String(required=True)
    password = String(required=True)


@auth.verify_token
def verify_token(token: str):
    if not token:
        return None
    try:
        payload = jwt.decode(
            token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
        )
    except jwt.exceptions.InvalidSignatureError:
        return None
    email = payload.get("email")
    if email:
        user = db.session.query(User).filter(User.email == email).first()
        if user:
            return user


@login_api.post("/login")
@login_api.input(LoginIn)
def login(data):
    user = db.session.query(User).filter(User.email == data["email"]).first()
    if not user:
        abort(404)
    payload = {"email": user.email}
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return {"token": token}
