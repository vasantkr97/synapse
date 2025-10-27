import os
from fastapi import FastAPI, Request
from typing import Any, Dict

app = FastAPI()

@app.get("/health")
async def health_check(request: Request) -> Dict[str, Any]:
    