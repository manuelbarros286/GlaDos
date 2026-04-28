from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router

app = FastAPI(title="GlaDos API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # allow any for now
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def health_check():
    return {"status": "online", "message": "GlaDos is operational!"}
