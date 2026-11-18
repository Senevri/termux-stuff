import os
import logging
import httpx2

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import StreamingResponse, Response
from starlette.background import BackgroundTask
from starlette.routing import Route

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("proxy")

BACKEND = os.getenv("PROXY_URL", "http://localhost:11434")

#for testing only:
BACKEND = "http://100.86.150.46:8000"

client = httpx2.AsyncClient(timeout=None, trust_env=False)


async def proxy(request: Request):
    logger.info(f"Using backend {BACKEND}")
    url = BACKEND + request.url.path

    if request.url.query:
        url += "?" + request.url.query

    try:
        upstream_request = client.build_request(
            request.method,
            url,
            content=await request.body(),
        )

        logger.info(upstream_request.content)

        upstream = await client.send(upstream_request, stream=True)

        response = StreamingResponse(
            upstream.aiter_raw(),
            status_code=upstream.status_code,
            background=BackgroundTask(upstream.aclose),
        )
        logger.info(f"Response: {response}")
        return response

    except httpx2.ConnectError:
        logger.exception("Backend connection failed: %s", url)
        return Response("Bad Gateway", status_code=502)


app = Starlette(routes=[
    Route("/{path:path}", proxy, methods=[
        "GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"
    ]),
])
