import uvicorn
from fastapi import FastAPI

from database.connection import Settings
from routes import users, videos

app = FastAPI()
settings = Settings()
app.include_router(users.router, prefix="/user")
app.include_router(videos.router, prefix="/video")


@app.on_event("startup")
async def init_db():
    await settings.initialize_database()


@app.get("/")
async def root():
    return {"message": "Hello YongFLIX!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
