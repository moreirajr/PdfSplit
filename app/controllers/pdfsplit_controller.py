import imp
import logging
import gc
import json
from pkgutil import ImpImporter
from fastapi import (APIRouter, HTTPException, File, UploadFile, Form, Depends, Request, BackgroundTasks)
from fastapi.encoders import jsonable_encoder
from app.services.splitfile_service import SplitFileService
from starlette import status
from starlette.responses import Response, JSONResponse, RedirectResponse, HTMLResponse

router = APIRouter()
logger = logging.getLogger(__name__)
splitfileService = SplitFileService()

def ErrorMessage(message: str, statuscode: status):
    return JSONResponse(content={"Error": message },
        media_type="application/json",
        status_code=statuscode)

@router.post("/split-async", name="Quebra de pdf async", status_code=status.HTTP_200_OK)
async def split_file_async(request: Request,
    background_tasks: BackgroundTasks,
    num_pages: int = Form(..., description="Páginas por pdf"),
    filename: str = Form(..., description="Nome do arquivo"),
    file: UploadFile = File(..., description="Arquivo enviado")):
    
    try:
        if not file.filename.lower().endswith(('.pdf')):
            return ErrorMessage("File must be .pdf", status.HTTP_400_BAD_REQUEST)

        if not filename.lower().endswith(".zip"):
            filename = filename + ".zip"

        logger.debug("Processing " + filename + " with num pages " + str(num_pages))     
               
        fileType = await file.read(10)
        if "pdf" not in str(fileType.lower()):
            return ErrorMessage("File is not a valid .pdf", status.HTTP_400_BAD_REQUEST)

        await file.seek(0)
        file_content = await file.read()
        pdfObj = splitfileService.split(filename, file.filename, num_pages, file_content)
        
        response = Response(pdfObj, media_type="application/x-zip-compressed", headers={
            'Content-Disposition': f'attachment;filename={filename}'})

        return response
    except Exception as ex:
        logger.exception(ex)
        return ErrorMessage(str(ex), status.HTTP_500_INTERNAL_SERVER_ERROR)