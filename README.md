# FastAPI Tour

A FastAPI sample application to learn how to use FastAPI with SQLAlchemy and PostGreSQL.

# Sample Setup

- Create a virtual environment using `virtualenv` module in python.

```bash
# Install module (globally)
pip install virtualenv

# Generate virtual environment
virtualenv --python=3.11.9 venv

# Activate virtual environment
source venv/bin/activate # on Mac/Linux
venv\Scripts\activate # on Windows

# Install depdendency packages
pip install fastapi
pip install "uvicorn[standard]"
pip install sqlalchemy
pip install psycopg2-binary
pip install alembic
pip install passlib
pip install asyncpg
pip install python-jose
pip install python-multipart
pip install pylint
pip install bcrypt
# export dependencies package to requirements file
# pip freeze > requirements.txt
# pip install -r requirements.txt
```

- Configure `.env` file by creating a copy from `.env.sample`
- Generate JWT secret

```bash
python
import secrets
secrets.token_hex(16)
```

- Setup a postgres docker container

```bash
docker run -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=<your-preferred-one> -d postgres:14

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
