import uvicorn

from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        app_dir="app",
        host='0.0.0.0',
        port=settings.APP_PORT,
        reload=settings.APP_RELOAD,
    )