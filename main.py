from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import logging
import uvicorn
from typing import Dict
import quandl
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
#from authentication.registered_users import registered_users

app = FastAPI()
security = HTTPBasic()

####################### Configure logging #######################

logging.basicConfig(level=logging.INFO)

quandl.ApiConfig.api_key = 'xicuz9aHTaJpEVeQx6Lf'

class Price(BaseModel):
     def __call__(self):
        simbolo: str
        nome_da_empresa: Union[str, None] = None
        price: float
        tax: Union[float, None] = None

class RegisteredUsers:
    def __init__(self, users: Dict[str, str]):
        self.users = users

    # Torna a classe chamável como uma função
    def __call__(self, username: str) -> str:
        return self.users.get(username)  # Usa o dicionário interno diretamente

# Instanciando a classe RegisteredUsers
registered_users = RegisteredUsers({
    "user1": "secret1",
    "user2": "secret2"
})


####################### BASIC AUTHENTICATION #######################


def verify_user(credentials: HTTPBasicCredentials = Depends(security)):
    # Agora usamos registered_users como um objeto chamável
    correct_password = registered_users(credentials.username)
    
    if not correct_password or correct_password != credentials.password:
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


####################### ROUTES #######################
    

@app.get("/")
async def home(home: Annotated[str, Depends(registered_users)]):
    logging.debug("Root endpoint accessed")
    logging.info("Testing Info")
    logging.warn("Testing Warning")
    logging.error("Testing Error")
    return {"Teste": "1 - Jhayne Ketleen"}

@app.get("/users")
async def users(username: Annotated[str, Depends(registered_users)]):
    logging.info(f"User {username} requested")
    return {"username": username}

@app.get("/users/{id_user}")
async def read_current_user(username: Annotated[str, Depends(registered_users)]):
    logging.info(f"User {username} requested users")
    return {"username": username}

@app.get("/price", response_model=Dict)
async def get_price(username: str = Depends(verify_user)):
    try:
        # Obtém os dados da Quandl
        mydata = quandl.get("WSE/WIG20TR")

        # Extrai o preço de fechamento mais recente
        close_price = mydata['Close'].iloc[-1]

        # Log do usuário requisitante
        logging.info(f"Usuário {username} solicitou o preço de fechamento")

        # Retorna o preço de fechamento mais recente
        return {"username": username, "close_price": close_price}
    
    except quandl.errors.quandl_error.NotFoundError:
        raise HTTPException(status_code=404, detail="Dados não encontrados na API do Quandl")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar dados da API do Quandl: {str(e)}")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)