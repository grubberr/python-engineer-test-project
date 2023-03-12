from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


user_to_team = db.Table(
    "user_to_team",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("team_id", db.Integer, db.ForeignKey("team.id")),
)


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    users = db.relationship("User", backref="company")
    teams = db.relationship("Team", backref="company")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Team(db.Model):
    __table_args__ = (
        db.UniqueConstraint("name", "company_id"),
    )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    members = db.relationship(User, secondary=user_to_team, backref="teams")
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
