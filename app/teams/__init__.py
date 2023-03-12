from apiflask import APIBlueprint, Schema, abort
from apiflask.fields import Integer, List, Nested, String
from apiflask.validators import Length
from sqlalchemy.exc import IntegrityError

from app.model import Company, Team, User, db
from app.teams.auth import auth

api = APIBlueprint("api", __name__)


class CompanySchema(Schema):
    id = Integer(required=True)
    name = String(required=True)


class UserSchema(Schema):
    id = Integer(required=True)
    name = String(required=True)
    company = Nested(CompanySchema)


class TeamSchema(Schema):
    id = Integer(required=True)
    name = String(required=True)
    members = List(Nested(UserSchema), required=True, validate=Length(min=2))


class TeamNew(Schema):
    name = String(required=True)
    members = List(Integer(), required=True, validate=Length(min=2))


class TeamsResponse(Schema):
    teams = List(Nested(TeamSchema))


class TeamResponse(Schema):
    team = Nested(TeamSchema)


class TeamsRequest(Schema):
    company = String()


@api.get("/teams")
@api.auth_required(auth)
@api.input(TeamsRequest, location="query")
@api.output(TeamsResponse)
def get_teams(data):
    query = db.session.query(Team)
    company = data.get("company")
    if company:
        query = query.join(Company).filter(Company.name == company)
    return {"teams": query}


@api.get("/team/<int:team_id>")
@api.auth_required(auth)
@api.output(TeamResponse)
def get_team(team_id):
    team = db.session.query(Team).get(team_id)
    if not team:
        abort(404)
    return {"team": team}


@api.post("/team")
@api.auth_required(auth)
@api.input(TeamNew)
def create_team(data):
    user_ids = set()
    company_ids = set()
    members = []
    for user in db.session.query(User).filter(User.id.in_(data["members"])):
        user_ids.add(user.id)
        company_ids.add(user.company_id)
        members.append(user)

    unknown_user_ids = list(set(data["members"]) - user_ids)
    if unknown_user_ids:
        abort(400, f"members: {repr(unknown_user_ids)} not found")

    if len(company_ids) > 1:
        abort(400, f"members: {repr(data['members'])} belong to different companies")

    company_id = company_ids.pop()
    team = Team(name=data["name"], members=members, company_id=company_id)
    db.session.add(team)

    try:
        db.session.commit()
    except IntegrityError:
        abort(409, f"team name: {data['name']} already exists")

    return {"id": team.id}
