from fastapi import FastAPI
from uvicorn import run as uvicorn_run
from api import router


app = FastAPI(title='Multitasker')
app.include_router(router)

if __name__ == '__main__':
    uvicorn_run('main:app', reload=True)
