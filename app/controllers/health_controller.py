import logging
from fastapi import (APIRouter, HTTPException, File, UploadFile, Form, Depends, Request, BackgroundTasks)
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import Response, JSONResponse, RedirectResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("", name="Healthcheck", status_code=status.HTTP_200_OK)
def healthcheck(request: Request):
    response = JSONResponse(content={ "Status": "healthy" },
        media_type="application/json",
        status_code=status.HTTP_200_OK)

    return response