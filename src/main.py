import uvicorn
from fastapi import FastAPI

from database.connection import Settings
from routes.users import router

app = FastAPI()
settings = Settings()
app.include_router(router, prefix="/user")


@app.on_event("startup")
async def init_db():
    await settings.initialize_database()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
