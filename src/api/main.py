from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.routes import router as v1_router
from scalar_fastapi import get_scalar_api_reference
app = FastAPI(
    title="GlaDos Intelligence",
    version="1.0.0",
    description="Strategic OSINT Analysis & Trend Detection"
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time

    print(f"Request: {request.method} {request.url.path} - Processed in {process_time:.4f}s")
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

origins= [
    "http://localhost:5173",
    "http://127.0.0.1:8080",
    "https://glados-ui.vercel.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # allow only our frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from mangum import Mangum

handler = Mangum(app) # AWS Lambda call

import time
from fastapi import Request


app.include_router(v1_router, prefix="/api/v1", tags=["v1"])
@app.get("/")
async def root():
    return {
        "project": "GlaDos",
        "api_versions": ["v1"],
        "docs": "/scalar"
    }

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )