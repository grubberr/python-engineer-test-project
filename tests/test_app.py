import jwt
from werkzeug.security import generate_password_hash

from app.model import Company, Team, User, db


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


def test_create_team(app):
    with app.app_context():
        company1 = Company(name="CentralNic")
        user1 = User(name="Tory Smith", email="tory.smith@domain.com", company=company1)
        user1.password = generate_password_hash("password")
        user2 = User(name="Sienna Brittny", email="sienna.brittny@domain.com", company=company1)
        user2.password = generate_password_hash("password")
        company2 = Company(name="GoDaddy")
        user3 = User(name="Anderson Hudson", email="anderson.hudson@domain.com", company=company2)
        user3.password = generate_password_hash("password")
        db.session.add_all([user1, user2, user3])
        db.session.commit()
        user1_id, user2_id, user3_id = user1.id, user2.id, user3.id

    payload = {"email": "tory.smith@domain.com"}
    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")

    client = app.test_client()
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/team", headers=headers, json={"name": "Team1", "members": [user1_id]})
    assert response.status_code == 422
    assert response.json["detail"]["json"]["members"][0] == "Shorter than minimum length 2."

    response = client.post(
        "/team",
        headers=headers,
        json={"name": "Team1", "members": [user1_id, user3_id]},
    )
    assert response.status_code == 400
    assert response.json["message"] == "members: [1, 3] belong to different companies"

    response = client.post(
        "/team", headers=headers, json={"name": "Team1", "members": [user1_id, 100]}
    )
    assert response.status_code == 400
    assert response.json["message"] == "members: [100] not found"

    response = client.post(
        "/team",
        headers=headers,
        json={"name": "Team1", "members": [user1_id, user2_id]},
    )
    assert response.status_code == 200
    assert response.json["id"] == 1

    response = client.post(
        "/team",
        headers=headers,
        json={"name": "Team1", "members": [user1_id, user2_id]},
    )
    assert response.status_code == 409
    assert response.json["message"] == "team name: Team1 already exists"

    with app.app_context():
        teams = db.session.query(Team).all()
        assert len(teams) == 1
        assert teams[0].name == "Team1"
        assert len(teams[0].members) == 2
        assert {user.id for user in teams[0].members} == {user1_id, user2_id}
