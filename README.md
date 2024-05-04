# Simple Ecommerce Application

- Clone the repository
- Install dependencies:
```bash
pip install -r requirements.txt
```

- Set up environment variables:
```bash
cp .env.example .env
```

- Update .env with your PostgreSQL database credentials and other configurations.

- Make sure there is a database named `ecom` in your postgres instance.

- Generate migrations:
```bash
alembic init alembic
alembic revision --autogenerate -m "init"
```
- NOTE: If running alembic command outside docker env, then change the `DATABASE_HOST` env variable to `localhost`

- Run migrations:
```bash
alembic upgrade head
```

- Start the FastAPI server: (Project uses makefile so ensure make cli is installed)
- Make sure `DATABASE_HOST` value is set to `db` here
```bash
make restart
```
