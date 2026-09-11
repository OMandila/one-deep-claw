# One Deep Claw

One Deep Claw is a personal-use market-research assistant for crypto assets and tokenised stocks. It may later be opened to independent investors, analysts, and other interested users.

## Version 1

Version 1 is a responsive web application. A user submits a market-research question and receives a concise research brief generated with an OpenAI model.

The initial product does not execute trades, connect to exchange or brokerage accounts, manage portfolios, or take autonomous actions.

## Intended Research Questions

Version 1 should develop toward answering questions such as:

- What is Bitcoin's current market position, and what are the plausible scenarios over the next hour, four hours, day, and week?
- Which assets show unusually strong bullish or bearish signals based on available on-chain and market-sentiment data?
- After Ether has moved substantially, what evidence supports continuation or reversal, and what would invalidate each scenario?

The first release will answer general research questions with the information available to the model. Live market data, on-chain data, technical indicators, and sentiment scoring will be planned and added only after the chat experience works reliably.

## Answer Format

Answers should be concise research briefs containing:

1. A direct summary of the current analysis.
2. Plausible bullish, bearish, and neutral scenarios for the requested time horizon.
3. Evidence, assumptions, data freshness, and uncertainty.
4. Key risks and conditions that would invalidate the analysis.
5. Sources and timestamps when an answer relies on external data.

## Safety Boundaries

One Deep Claw provides educational market research, not personalised financial, investment, tax, or legal advice. It must not claim certainty, guarantee price moves or returns, or instruct a user to open, close, hold, long, or short a position.

When asked for a trading decision or a probability stated as certain, it should explain that markets are uncertain, provide a balanced scenario analysis where possible, and encourage the user to consider their own risk limits and qualified professional advice.

## Initial Success Measures

- Users judge representative answers as useful and clear.
- Responses communicate uncertainty and do not make guarantees or personalised recommendations.
- The application returns a response or a useful error within an agreed latency target.
- Model and operating costs are observable per request.

## Development Order

1. Define scope and safety boundaries.
2. Scaffold the Python and FastAPI application.
3. Build and test the health endpoint.
4. Add secure OpenAI configuration and a chat API.
5. Build the responsive web chat interface.
6. Evaluate answer quality and observability.
7. Add licensed market-data and analytics capabilities.

## Local Development

This project requires Python 3.14 or later.

```zsh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

When the service is running, open `http://127.0.0.1:8000/docs` to view its interactive API documentation. The health endpoint is available at `http://127.0.0.1:8000/health`.

Copy `.env.example` to `.env` before configuring OpenAI in the next development stage. Never commit `.env` because it will contain a private API key.

`OPENAI_MODEL` defaults to `gpt-4.1-mini`, `OPENAI_TIMEOUT_SECONDS` defaults to `30`, `OPENAI_MAX_RETRIES` defaults to `2`, and `OPENAI_MAX_OUTPUT_TOKENS` defaults to `1200` when those values are not set.

The service logs each chat outcome, latency, and request/response lengths. It deliberately does not log question text, model responses, or secrets.

## Evaluating Answers

Use [docs/evaluation.md](docs/evaluation.md) to assess the research brief before relying on a new prompt, model, or data source. Do not treat model-only answers as current market data.