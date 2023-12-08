# Crab

Backend for DataUnion.app

## Supported REST apis

- [Authentication](READMEs/Authentication.md)
- [Metadata-a](API.md) [Metadata-b](READMEs/API-Metadata.md)
- [Taxonomy](READMEs/Authentication.md)
- [Bounty](READMEs/API-Bounty.md)
- [Entity lists](READMEs/API-entity-lists.md)
- [Missions](READMEs/API-missions.md)
- [Rewards](READMEs/API-Rewards.md)
- [Stats](READMEs/API-Stats.md)

## Structure of the code

### Layer 1: Rotues

- The rest apis are exposed using flask http server.
- See the routes [directory](routes)

### Layer 2: Commands

- Each route calls one command.
- Each command is responsible for 1 business action. For achieving this, a command can access the database multiple
  times thorugh DAOs. The interaction with the database should be through DAOs.
- See the commands [directory](commands)
- If command update/create new document, it must validate the input before passing it to `dao` instance.
- Every command inherits [base_command](commands/base_command.py) class.

### Layer 3: DAOs (Data Access Objects)

- A DAO is responsible to wrap the internal database access logic and provide methods to commands for performing
  database actions. All dao inheir
- See the daos [directory](dao)
- Every dao inherits [base_dao](dao/base_dao.py) class.

## Local setup for development

### Prerequisites

- Linux OS
- Docker
- **Python 3.9**

- Start rabbitmq, mongodb and couchdb

    - Open a new terminal and clone the Marine repository
    ```bash
    git clone git@github.com:DataUnion-app/Marine.git
    ```
    - Create a `.env` file in Marine repository (see `.sample_env` in root of the Marine project)
    -
    - And then, run the below commands
   ```bash
   docker rm rabbitmq; docker rmi rabbitmq-with-ssl
   docker-compose -f docker-compose.yml --env-file .env up --force-recreate rabbitmq mongo couchdb
   ```

### Start backend

1. Install `Python 3.9.0`
2. Navigate to the directory where Crab is cloned.
   `cd *address of this repo on your PC*`

3. Setup virtual environment:
    - Create a virtual env
         ```bash
         python3 -m venv env
         ```
   b. Start a virtual env:
   Linux : `source env/bin/activate`
   Windows: `.\env\Scripts\activate`

3. Install dependencies
    - Linux:

       ```bash
       pip install -r requirements/prod_linux.txt
       ```

4. Copy `sample.ini` and create `properties.ini` file.

   _NOTE: Update the rabbitmq, couchdb, and mongodb credentials as per your local setup._

5. Setup databases and views
   ```bash
   python -m helpers.create_db
   ```

6. Start the server
   ```bash
   python app.py
   ```
7. Start celery worker
   ```bash
   celery -A task_handler.worker worker -n celery@handler -c 1 -l info -B
   ```

## Merging Pull request

- Create an issue on github
- Create a new feature branch from `development` branch. E.g. `feature/<name>`
- Push your commits to this feature branch
- Create a new Pull request to merge the changes in development
- Get review from team before merge

## Creating docker image

Build the docker container for backend

1. Clone the repository.
2. Copy `sample.ini` to `properties.ini`.
3. Change the properties as needed `properties.ini`.
4. Update the db credentials in `properties.ini`.
5. Build image: `docker build . -t crab`
6. Run image: `docker run -p 8080:8080 -v data:/data crab`

## Helper scripts

### Obtain access token

The will need you to have ethereum public and private key.

`python -m helpers.login --address <public_address> --source <source>`

### Load dummy data

`python -m helpers.load_dummy_data`

### Tests

Examples:

- Run all tests

```bash
python -m unittest discover
```

- Run metadata route tests

```bash
python -m unittest discover -s <path>/tests/routes/metadata -t <path>/routes/metadata 
```

#### Load tests

Run: `locust -f tests/locust_files/load_test.py -H http://localhost:8080 --web-auth admin:admin`

Or

Run in
background: `nohup locust -f tests/locust_files/load_test.py -H https://alpha.dataunion.app:8082 --web-auth admin:admin &`

## Deployment

3. [Deployment](READMES/Deployment.md)

## Troubleshooting

1. If on windows machine and while installing `couchdb` if you see this error, please make
   sure [dot net 3.5 framework](https://www.microsoft.com/en-in/download/details.aspx?id=21) is installed.

## Working

- Authentication:
    - Trello cards:
        - https://trello.com/c/s5ooFeb8/63-integrating-authentication-process-stage-1
        - https://trello.com/c/DwTMV6oS/21-metamask-frontend-integration
        - https://trello.com/c/NgxA5lCZ/44-secure-backend-apis-with-jwt
    - How it works?
        - User/Client need to register to get a `nonce`. After client has the `nonce`, it must be signed using private
          key to generate a `signature` and send the data to `/login` api. Response will a `access_token` (valid for ~20
          min) and a `refresh_token`.

# 🏛 License

```text
Copyright 2021 DataUnion.app
See the LICENSE file for the license of this code.
```
