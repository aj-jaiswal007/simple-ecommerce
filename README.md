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
pip install alembic
alembic init alembic
alembic revision -m “First commit”
```

- Run migrations:
```bash
alembic upgrade head
```

- Start the FastAPI server: (Project uses makefile so ensure make cli is installed)
```bash
make restart
```
