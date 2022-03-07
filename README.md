# Project Setup

[![Production Workflow](https://github.com/kc446/kc446_flaskapp/actions/workflows/prod.yml/badge.svg)](https://github.com/kc446/kc446_flaskapp/actions/workflows/prod.yml)

* [Production Deployment](https://kc446-flaskapp.herokuapp.com/)

[![Development Workflow](https://github.com/kc446/kc446_flaskapp/actions/workflows/dev.yml/badge.svg)](https://github.com/kc446/kc446_flaskapp/actions/workflows/dev.yml)

* [Developmental Deployment](https://kc446-flaskapp.herokuapp.com/)

## Setting up CI/CD

The result of this will be that when you create a pull request to merge a branch to master, it will deploy to your
heroku development app/dyno and when you merge or push to master on github, it will deploy the app to the production heroku
app/dyno.
### Instructions

-[x] Clone this repo to your local (DO NOT FORK THIS REPO, IF YOU DO YOU HAVE TO ENABLE ACTIONS BEFORE ANYTHING RUNS)
-[x] Create a new repo on your own account
-[x] Remove the origin remote and replace it with your own new repo.  (Do not add a readme or anything it should be empty)
-[x] Create an account with Heroku, create an app for production and an app for development
-[x] Create a new repo in Docker hub

#### Setup Docker and Heroku Credentials In the Repository Settings under Action -> Secret

-[x] Add repository settings for action secrets for DOCKER_USERNAME, DOCKER_PASSWORD, HEROKU_API_KEY (put the appropriate
   values in)
### GitHub Notes:  Set the action secrets repository in: -> settings -> actions -> secrets
### Heroku Notes: Get the heroku API key from account in: -> applications -> create authorization button

#### Change GitHub Actions Workflows for Dev and Prod

-[x] Change line 42 to have your docker repo address in: .github/workflows/prod.yml
-[x] change lines 58 to have your heroku app name in: .github/workflows/prod.yml
-[x] change line 59 to have your heroku email in: .github/workflows/prod.yml
-[x] change line 31 to have your heroku app name in .github/workflows/dev.yml
-[x] change line 32 to have your heroku email in .github/workflows/dev.yml
-[ ] Push your local repo and fix any errors that appear when the workflow is running. You can check the workflow in the
    actions.

## Running Locally

1. To Build with docker compose:
   docker compose up --build
2. To run tests, Lint, and Coverage report use this command: pytest --pylint --cov

.pylintrc is the config for pylint .coveragerc is the config for coverage setup.py is a config file for pytest


### Future Notes and Resources
* https://flask-user.readthedocs.io/en/latest/basic_app.html
* https://hackersandslackers.com/flask-application-factory/
* https://suryasankar.medium.com/a-basic-app-factory-pattern-for-production-ready-websites-using-flask-and-sqlalchemy-dbb891cdf69f
