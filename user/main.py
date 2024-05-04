from dotenv import load_dotenv
from fastapi import FastAPI

from common.heartbeat import router as heartbeat_router
from user import routes as user_routes

load_dotenv()
app = FastAPI(
    title="Ecommerce Auth Service",
    description="Ecommerce Auth Service to generate tokens",
    version="0.1.0",
)
app.include_router(user_routes.public_routes)
app.include_router(user_routes.authenticated_routes)
app.include_router(heartbeat_router)
