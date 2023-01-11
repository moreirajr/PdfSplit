from email.policy import default
from lib2to3.pytree import Base
import os
from decouple import config
import logging


logger = logging.getLogger(__name__)
baseDir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig():
    TEST = False
    DEBUG = False

    PROJECT_VERSION = 'v1'
    PROJECT_NAME = 'Api de SPlit de Pdfs'
    PROJECT_DESCRIPTION = 'Serviço para split de arquivos pdf'

    BASE_URL = config("BASE_URL", default="http://localhost:8000/")
    API_PREFIX = config('API_PREFIX', default='')
    
    logger.debug(BASE_URL)

    def init_app(self, app):
        app.config = self

class DevelopmentConfig(BaseConfig):
    name = 'development'
    DEBUG = True

class TestsConfig(BaseConfig):
    name = 'tests'
    TESTING = True
    DEBUG = True
    
class ProductionConfig(BaseConfig):
    name = 'production'
    DEBUG = False

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class AppConfig(metaclass=SingletonMeta):
    def __init__(self, name):
        self._name = name
        self._config = dict(dev=DevelopmentConfig, tests=TestsConfig, prod=ProductionConfig)

    @property
    def config(self):
        return self._config[self._name]()