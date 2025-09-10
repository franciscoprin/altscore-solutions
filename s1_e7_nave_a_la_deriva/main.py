from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

app = FastAPI(title="S1 E7 - Nave a la Deriva")

templates = Jinja2Templates(directory="templates")

logger = logging.getLogger("app")
logging.basicConfig(level=logging.INFO)

system_code_map = {
  "navigation": "NAV-01",
  "communications": "COM-02",
  "life_support": "LIFE-03",
  "engines": "ENG-04",
  "deflector_shield": "SHLD-05"
}

choosen_system = "engines"

async def log_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = int((start - time.time()) * -1000)
    logger.info(
        "%s %s UA=%s -> %s in %dms",
        request.method,
        request.url.path,
        request.headers.get("user-agent"),
        response.status_code,
        duration_ms,
    )
    return response

app.middleware("http")(log_requests)


@app.get("/status")
async def status(request: Request):
    return {
        "damaged_system": choosen_system
    }

@app.get("/repair-bay")
async def repair_bay(request: Request):
    damaged = system_code_map[choosen_system]
    return templates.TemplateResponse(
        "repair_bay.html",
        {"request": request, "damaged": damaged}
    )

@app.post("/teapot")
async def teapot():
    raise HTTPException(status_code=418, detail="I'm a teapot")


@app.get("/healthz")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
