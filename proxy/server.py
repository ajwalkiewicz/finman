#!/usr/bin/env python3

import json
import logging
import os
from datetime import date, datetime
from typing import Literal, cast

import httpx
import redis
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic Models
supported_currencies = Literal["USD", "EUR", "PLN", "GTQ"]


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    redis: Literal["connected", "disconnected"]


class Rates(BaseModel):
    timestamp: int
    base: str
    date: str
    rates: dict[supported_currencies, float]


class RatesResponse(Rates):
    success: bool


class FixerAPIBaseModel(BaseModel):
    success: bool


class FixerAPIResponseSuccess(FixerAPIBaseModel):
    timestamp: int
    base: Literal["EUR"]
    date: str
    rates: dict[supported_currencies, float]


class FixerAPIResponseError(FixerAPIBaseModel):
    error: dict


# Load environment variables
load_dotenv("/app/data/.env")
FIXER_API_KEY = os.getenv("FIXER_API_KEY")
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

if not FIXER_API_KEY:
    logger.error("FIXER_API_KEY not found in env file")
    raise ValueError("FIXER_API_KEY not found in env file")

allowed_origins = [
    "http://localhost:3000",
    "http://finman.walkiewicz.io",
    "https://finman.walkiewicz.io",
]

logger.info(f"Allowed origins: {allowed_origins}")

# Initialize FastAPI app
app = FastAPI(title="Exchange Rate Proxy", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis setup
try:
    redis_client = redis.Redis(
        host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True
    )
    redis_client.ping()
    logger.info("Client: %s", redis_client)
    logger.info("Connected to Redis")
except redis.ConnectionError:
    logger.error("Could not connect to Redis. Make sure Redis is running.")
    exit(1)

# Cache configuration
CACHE_KEY_PREFIX = "exchange_rates"
CACHE_DURATION = 24 * 60 * 60  # 24 hours in seconds


def get_today_cache_key():
    """Generate cache key for today's exchange rates"""
    today = date.today().isoformat()
    return f"{CACHE_KEY_PREFIX}_{today}"


def calculate_rates_with_base(
    eur_rates: FixerAPIResponseSuccess, new_base: supported_currencies
) -> RatesResponse:
    """
    Calculate exchange rates with a different base currency

    Args:
        eur_rates (RatesModel): Exchange rates with EUR as base
        new_base (str): New base currency code

    Returns:
        RatesModel: Exchange rates with new base currency
    """
    if new_base not in eur_rates.rates:
        raise ValueError(f"Currency {new_base} not found in rates")

    base_rate = eur_rates.rates[new_base]
    new_rates = {}

    for currency, rate in eur_rates.rates.items():
        new_rates[currency] = rate / base_rate

    return RatesResponse(
        success=eur_rates.success,
        timestamp=eur_rates.timestamp,  # Preserve original timestamp
        base=new_base,
        date=eur_rates.date,  # Preserve original date
        rates=new_rates,
    )


def fetch_from_fixer_api() -> FixerAPIResponseSuccess:
    """Fetch exchange rates from Fixer API"""
    url = "https://data.fixer.io/api/latest"
    params = {"access_key": FIXER_API_KEY, "symbols": "USD,EUR,PLN,GTQ"}

    try:
        response = httpx.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        logger.info("Data fetched from Fixer API: %s", data)

        if not data.get("success", False):
            data = FixerAPIResponseError.model_validate(data)
            raise Exception(f"Fixer API error: {data.error}")

    except httpx.HTTPError as e:
        logger.error(f"Error fetching from Fixer API: {e}")
        raise

    return FixerAPIResponseSuccess.model_validate(data)


@app.get("/api/rates", response_model=RatesResponse)
def get_exchange_rates(base: supported_currencies = "PLN"):
    """Get exchange rates with optional base currency conversion"""
    base_currency = base
    today_key = get_today_cache_key()

    # Check cache first
    cached_data = cast(str | None, redis_client.get(today_key))

    if cached_data:
        logger.info("Using cached exchange rates from %s", today_key)
        eur_based_rates = FixerAPIResponseSuccess.model_validate(
            json.loads(cached_data)
        )
    else:
        logger.info("Fetching fresh exchange rates from Fixer API")
        eur_based_rates = fetch_from_fixer_api()

        # Cache the EUR-based rates
        redis_client.setex(today_key, CACHE_DURATION, eur_based_rates.model_dump_json())
        logger.info("Cached exchange rates for today")

    # If base currency is EUR, return as-is
    if base_currency == "EUR":
        return eur_based_rates

    # Calculate rates with requested base currency
    converted_rates = calculate_rates_with_base(eur_based_rates, base_currency)
    return converted_rates


@app.get("/health")
def health_check():
    """Health check endpoint"""
    try:
        redis_client.ping()
        redis_status = "connected"
    except Exception:
        redis_status = "disconnected"

    return JSONResponse(
        content={
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
            "redis": redis_status,
        }
    )


if __name__ == "__main__":
    logger.info("Starting exchange rate proxy server...")
    logger.info(f"Fixer API Key: {'*' * (len(FIXER_API_KEY) - 4)}{FIXER_API_KEY[-4:]}")

    # Use 0.0.0.0 to accept connections from outside the container
    uvicorn.run(app, host="0.0.0.0", port=8012)
