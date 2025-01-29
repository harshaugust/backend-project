from fastapi import FastAPI
from routers import reviews

app = FastAPI()


app.include_router(reviews.router)
