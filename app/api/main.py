from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.api.routers.reflections import router as reflections_router
from app.api.routers.resources import router as resources_router
from app.api.routers.sessions import router as sessions_router
from app.api.routers.topics import router as topics_router
from app.api.routers.users import router as users_router
from app.business.errors import ConflictError, NotFoundError, ValidationError

# Hosting notes (Render):
# 1) Push this project to GitHub.
# 2) Create a new Render "Web Service" from that repo.
# 3) Build command: pip install -r requirements.txt
# 4) Start command: uvicorn app.api.main:app --host 0.0.0.0 --port $PORT
# 5) Add DATABASE_URL in Render environment variables.

app = FastAPI(
    title="LearningLog Service API",
    description="Service layer for Project 2 business methods.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.exception_handler(ValidationError)
def handle_validation_error(_: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


@app.exception_handler(NotFoundError)
def handle_not_found_error(_: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(ConflictError)
def handle_conflict_error(_: Request, exc: ConflictError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


@app.exception_handler(Exception)
def handle_unexpected_error(_: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Unexpected server error: {exc}"},
    )


app.include_router(users_router)
app.include_router(topics_router)
app.include_router(resources_router)
app.include_router(sessions_router)
app.include_router(reflections_router)

