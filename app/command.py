import click
from flask import Flask
from flask.cli import AppGroup
from app.model import db, Company, Team, User

command_cli = AppGroup("command")


@command_cli.command("init-db")
def init_db():
    db.create_all()
    if not Team.query.filter_by(name="DevOps").first():
        company1 = Company(name="CentralNic")
        user1 = User(name="Tory Smith", email="torysmith@domain.com", company=company1)
        user2 = User(name="Sienna Brittny", email="siennabrittny@domain.com", company=company1)
        user3 = User(name="Anderson Hudson", email="andersonhudson@domain.com", company=company1)
        team1 = Team(name="DevOps", members=[user1, user2], company=company1)
        team2 = Team(name="Developers", members=[user1, user3], company=company1)
        company2 = Company(name="GoDaddy")
        user4 = User(name="Judy Moore", email="judymoore@domain.com", company=company2)
        team3 = Team(name="DevOps", members=[user4], company=company2)
        db.session.add_all([team1, team2, team3])
        db.session.commit()
