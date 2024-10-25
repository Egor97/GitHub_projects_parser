from logging import StreamHandler, basicConfig

from fastapi import FastAPI

from app.repos.router import router as repos_router

app = FastAPI()
app.include_router(repos_router, prefix='/api')


@app.on_event("startup")
def startup():
    x_format = '%(asctime)s : %(name)s : %(levelname)s : %(message)s'

    console_handler = StreamHandler()
    console_handler.setLevel('DEBUG')

    basicConfig(level='DEBUG', format=x_format, handlers=[console_handler])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
