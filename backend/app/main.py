from fastapi import FastAPI
from typing import Dict, Any

app = FastAPI()

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    return {"status": "healthy"}