# Python Engineer test project.

## Getting Started.

You should fork this repo and commit your changes to the forked version.  A running version is not a requirement though we will favour entires that we can run and interact with.

## The Task

You’ve been asked to implement a RESTFul API micro service that will let its users create and manage teams for companies used by our platform. The service should:

* support OpenAPI 3.0 specification
* accept JSON and return JSON responses


### Considerations
If given time, consider adding the following:

* Developer documentation
* JWT Authentication gateway
* GitHub Actions release pipeline


### Service Overview

Each team has an id, name and at least two members.
```
{
    'id': 1,
    'name': 'Engineering',
    'members': [
        {...}
    ]
}
```

Each team member is a `User` object that should have the following attributes:
```
{
    'id': 1,
    'name': 'John Doe',
    'email': 'john@doe.com',
    'company': {...}
}
```

Every User in the service belongs to one company which is made up of the following attributes:

```
{
    'id': 1,
    'name': 'Acme'
}
```

The service should make use of Flask and SqlAlchemy.  You can use any relational database of your choice to complete the task.

The service should support the following functionality:
* Create a new team
* View a list of all the teams
* View a list of all the teams for a specific company
* View a specific team


## Setting up

We've include a simple Dockerfile and basic flask app.py for you to start adding your code to

assuming you have docker set up and runing you can simple do the following to get started.

`docker compose build app`

`docker compose run --service-ports app`

After you have started the application you can run HTTP queries with help of `curl` to test the microservice.

To get the JWT token run the following:

```
export TOKEN=`curl -s -XPOST -H 'Content-Type: application/json' -d '{"email":"tory.smith@domain.com", "password":"password"}' http://localhost:5000/login | jq -r .token`
```

After receiving the JWT token you can run the main API HTTP requests.

To view a list of all the teams:

`curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/teams`

To view a specific team by id:

`curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/team/1`

To view teams for a specific company, you need to provide an additional optional query string parameter "company":

`curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/teams?company=GoDaddy`

To create a new team:

```
curl -XPOST -H 'Content-Type: application/json' -H "Authorization: Bearer $TOKEN" -d '{"name":"Programmers", "members":[1,2,3]}' http://localhost:5000/team
```
