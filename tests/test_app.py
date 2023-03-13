import jwt
from werkzeug.security import generate_password_hash

from app.model import Company, User, db


def test_login(app):
    with app.app_context():
        company = Company(name="CentralNic")
        user = User(name="Tory Smith", email="tory.smith@domain.com", company=company)
        user.password = generate_password_hash("password")
        db.session.add(user)
        db.session.commit()

    client = app.test_client()
    response = client.post("/login", json={"email": "tory.smith@domain.com", "password": "password"})
    assert "token" in response.json
    token = response.json["token"]
    payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    assert payload["email"] == "tory.smith@domain.com"
