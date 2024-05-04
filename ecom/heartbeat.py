from typing import Annotated

from fastapi import APIRouter, Depends

from ecom.common.logger import BoundLogger, get_logger

router = APIRouter()


@router.get("/heartbeat")
def heartbeat(logger: Annotated[BoundLogger, Depends(get_logger)]):
    logger.info("Heartbeat API called!")
    return {"status": "OK"}
