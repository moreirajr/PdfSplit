import logging
import time
import re
from app.controllers import pdfsplit_controller
from app.controllers import health_controller
from fastapi import FastAPI, Request
from app.core.config import AppConfig, TestsConfig

logger = logging.getLogger(__name__)


def create_app(config_name, cov=None):
    
    logger.debug(config_name)
    app_config = AppConfig(config_name).config

    app = FastAPI(title=app_config.PROJECT_NAME,
        description=app_config.PROJECT_DESCRIPTION,
        version=app_config.PROJECT_VERSION)
    
    #add middlewares
    #app.add_middleware( ... )

    app.include_router(pdfsplit_controller.router,
        prefix=f'{app_config.API_PREFIX}/v1/files', tags=['split'])

    app.include_router(health_controller.router,
        prefix=f'{app_config.API_PREFIX}/v1/health', tags=['healthcheck'])

    @app.middleware("http")
    async def coverage_middleware(request: Request, call_next):
        if type(app_config) is TestsConfig:
            start_time = time.time()
            response = await call_next(request)
            process_time = time.time() - start_time
            
            logger.debug(process_time)
        else:
            return await call_next(request)

    return app