from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

# Função que consulta uma API externa para obter cotações de ações
async def get_stock_price_from_external_api(stock_symbol: str) -> float:
    # Exemplo de uma URL para uma API externa (pode ser substituída por uma real)
    url = f"https://static.stooq.com/pp/w.js{stock_symbol}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return data['price']
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail="Erro ao consultar API de ações")
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Erro interno ao consultar API de ações")

@app.get("/price/{stock_symbol}")
async def get_stock_price(stock_symbol: str):
    price = await get_stock_price_from_external_api(stock_symbol)
    return {"stock_symbol": stock_symbol, "price": price}
