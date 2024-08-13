import httpx
from typing import Optional

API_URL = "https://stooq.com/t/?i=518"

async def get_stock_quote(symbol: str) -> Optional[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/{symbol}")
        if response.status_code == 200:
            return response.json()
        return None