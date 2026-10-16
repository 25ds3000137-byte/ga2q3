import os
import time
import uuid
from typing import Callable

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send

EMAIL = os.getenv("STUDENT_EMAIL", "25ds3000137@ds.study.iitm.ac.in")
ALLOWED_ORIGIN = "https://dash-iykobw.example.com"

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@api.get("/stats")
async def stats(values: str = Query(..., description="Comma-separated integers")):
    try:
        numbers = [int(item.strip()) for item in values.split(",")]
        if not numbers or any(item == "" for item in values.split(",")):
            raise ValueError
    except ValueError:
        raise HTTPException(status_code=400, detail="values must be comma-separated integers")

    total = sum(numbers)
    count = len(numbers)
    return {
        "email": EMAIL,
        "count": count,
        "sum": total,
        "min": min(numbers),
        "max": max(numbers),
        "mean": total / count,
    }

class RequestMetricsMiddleware:
    """Outer ASGI middleware so headers are attached to normal and CORS preflight responses."""
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = str(uuid.uuid4())
        started = time.perf_counter()

        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                elapsed = max(0.0, time.perf_counter() - started)
                headers = list(message.get("headers", []))
                headers.extend([
                    (b"x-request-id", request_id.encode("ascii")),
                    (b"x-process-time", f"{elapsed:.6f}".encode("ascii")),
                ])
                message["headers"] = headers
            await send(message)

        await self.app(scope, receive, send_with_headers)

app = RequestMetricsMiddleware(api)
