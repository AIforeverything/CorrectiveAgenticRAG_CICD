from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

# to add html and css to fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="CRAG", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    # allow_origins=[
    #     "http://localhost:5500",
    #     "http://127.0.0.1:5500",
    # ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

app.mount(
    "/",
    StaticFiles(directory="frontend", html=True),
    name="frontend",
)
