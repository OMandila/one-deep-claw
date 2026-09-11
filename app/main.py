from typing import Annotated
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAIError
from pydantic import BaseModel, Field

from app.openai_client import OpenAIClient
from app.settings import ConfigurationError, get_settings

app = FastAPI(title="One Deep Claw", version="0.1.0")
STATIC_DIRECTORY = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIRECTORY), name="static")

RESEARCH_BRIEF_INSTRUCTIONS = """You are One Deep Claw, a crypto and tokenised-stock
market-research assistant. Give a concise educational research brief. State important
assumptions and uncertainty. Present plausible bullish, bearish, and neutral scenarios
when relevant, including what could invalidate each scenario. Do not claim certainty,
guarantee price moves or returns, or give personalised instructions to buy, sell, hold,
long, or short an asset. Clearly say when you do not have current market, on-chain, or
sentiment data. This is research information, not financial, investment, tax, or legal
advice."""


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4_000)


class ChatResponse(BaseModel):
    response: str


def get_openai_client() -> OpenAIClient:
    return OpenAIClient(get_settings())


@app.exception_handler(ConfigurationError)
def configuration_error_handler(
    request: Request, error: ConfigurationError
) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"detail": "The research service is not configured yet."},
    )


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIRECTORY / "index.html")


@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    client: Annotated[OpenAIClient, Depends(get_openai_client)],
) -> ChatResponse:
    try:
        response = client.get_response(RESEARCH_BRIEF_INSTRUCTIONS, request.message)
    except OpenAIError as error:
        raise HTTPException(
            status_code=502,
            detail="The research service is temporarily unavailable. Please try again.",
        ) from error

    return ChatResponse(response=response)