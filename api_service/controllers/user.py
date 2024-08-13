from fastapi import FastAPI, HTTPException, Depends
import httpx

app = FastAPI()

# Simulação de um banco de dados de usuários
registered_users = {"stanleyjobson": "swordfish", "user2": "secret2"}

# Função para verificar se o usuário está registrado
def verify_user(username: str, password: str):
    if registered_users.get(username) != password:
        raise HTTPException(status_code=401, detail="Usuário não autorizado")

# Função para consultar o serviço interno de agregação de cotações
async def get_price_from_aggregator(stock_symbol: str) -> float:
    url = f"https://static.stooq.com/pp/g.js{stock_symbol}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Erro ao consultar serviço de agregação")
        return response.json()["price"]

@app.post("/quote/")
async def get_stock_quote(username: str, password: str, stock_symbol: str, 
                          user_verification: str = Depends(verify_user)):
    # Verifica o usuário
    verify_user(username, password)
    
    # Consulta o serviço interno de agregação de cotações
    price = await get_price_from_aggregator(stock_symbol)
    
    return {"user": username, "stock_symbol": stock_symbol, "price": price}
