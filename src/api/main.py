from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from scalar_fastapi import get_scalar_api_reference
app = FastAPI(title="GlaDos API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # allow any for now
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )