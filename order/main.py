from dotenv import load_dotenv
from fastapi import FastAPI

from common.heartbeat import router as heartbeat_router
from order.routes import authenticated_routes

load_dotenv()
app = FastAPI(
    title="Ecommerce Product Service",
    description="Ecommerce Product Service to manage products",
    version="0.1.0",
)
app.include_router(heartbeat_router)
app.include_router(authenticated_routes)
