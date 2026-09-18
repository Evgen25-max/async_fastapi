import logging
import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1 import films
from core.config import config
from core.logger import LOGGING
from db import elastic, redis

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Запуск приложения %s...', config.PROJECT_NAME_FASTAPI)
    redis.init_redis()
    elastic.init_elastic()

    try:
        await redis.get_redis().ping()
        logger.info('Redis доступен')
    except Exception as e:
        logger.warning('Redis недоступен при старте: %s', e)

    try:
        await elastic.get_elastic().info()
        logger.info("Elasticsearch доступен")
    except Exception as e:
        logger.warning('Elasticsearch недоступен при старте: %s', e)

    logger.info('Приложение запущено')

    yield
    logger.info('Остановка приложения')
    await redis.close_redis()
    await elastic.close_elastic()
    logger.info('Подключения закрыты')


app = FastAPI(
    title=config.PROJECT_NAME_FASTAPI,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    lifespan=lifespan,
)

app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
