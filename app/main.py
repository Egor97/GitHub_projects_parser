from logging import StreamHandler, basicConfig, getLogger

from fastapi import FastAPI

from app.database import create_connection_pool, close_connection_pool
from app.repos.router import router as repos_router

app = FastAPI()
app.include_router(repos_router, prefix='/api')

logger = getLogger(__name__)


@app.on_event('startup')
async def startup():
    x_format = '%(asctime)s : %(name)s : %(levelname)s : %(message)s'

    console_handler = StreamHandler()
    console_handler.setLevel('DEBUG')

    basicConfig(level='DEBUG', format=x_format, handlers=[console_handler])

    await create_connection_pool()


@app.on_event('shutdown')
async def shutdown():
    await close_connection_pool()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
