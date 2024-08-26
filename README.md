# FastAPI Tour

A FastAPI sample application to learn how to use FastAPI with SQLAlchemy and PostGreSQL.

# Sample Setup

- Create a virtual environment using `virtualenv` module in python.

```bash
# Install module (globally)
pip install virtualenv

# Generate virtual environment
virtualenv --python=<your-python-runtime-version> venv

# Activate virtual environment
source venv/bin/activate # on Mac/Linux
venv\Scripts\activate # on Windows

# Install depdendency packages
pip freeze > requirements.txt # export dependencies package to requirements file
# pip install -r requirements.txt
pip install fastapi
pip install "uvicorn[standard]"
pip install sqlalchemy
pip install psycopg2-binary
pip install alembic
```

- Configure `.env` file by creating a copy from `.env.sample`
- Setup a postgres docker container

```bash
docker run -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=<your-preferred-one> -d postgres:14
```

- At `app` directory, run `alembic` migration command. Please make sure your postgres DB is ready and accessible. In case you want to use `SQLite` instead, please be sure to configure the `env.py` file in `alembic` folder to support `batch execution` since `SQLite` does not support `ALTER` command, which is needed to configure the foreign key and establish the indexes.

```bash
# Init alembic folder
alembic init alembic

# Migrate to latest revison
alembic upgrade head

# Dowgragde to specific revision
alembic downgrade <revision_number>

# Downgrade to base (revert all revisions)
alembic downgrade base

# Create new revision
alembic revision -m <comment>
```

- Run `uvicorn` web server from `app` directory (`reload` mode is for development purposes)

```bash
uvicorn main:app --reload
```
