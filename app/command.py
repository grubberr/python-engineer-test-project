from flask.cli import AppGroup

from app.model import Company, Team, User, db

command_cli = AppGroup("command")


@command_cli.command("init-db")
def init_db():
    db.create_all()
    if not Team.query.filter_by(name="DevOps").first():
        company1 = Company(name="CentralNic")
        user1 = User(
            name="Tory Smith",
            email="tory.smith@domain.com",
            company=company1,
        )
        user1.set_password("password")
        user2 = User(
            name="Sienna Brittny",
            email="sienna.brittny@domain.com",
            company=company1,
        )
        user2.set_password("password")
        user3 = User(
            name="Anderson Hudson",
            email="anderson.hudson@domain.com",
            company=company1,
        )
        user3.set_password("password")
        team1 = Team(name="DevOps", members=[user1, user2], company=company1)
        team2 = Team(name="Developers", members=[user1, user3], company=company1)
        company2 = Company(name="GoDaddy")
        user4 = User(
            name="Judy Moore",
            email="judy.moore@domain.com",
            company=company2,
        )
        user4.set_password("password")
        user5 = User(
            name="Harry Potter",
            email="harry.potter@domain.com",
            company=company2,
        )
        user5.set_password("password")
        team3 = Team(name="DevOps", members=[user4, user5], company=company2)
        db.session.add_all([team1, team2, team3])
        db.session.commit()
