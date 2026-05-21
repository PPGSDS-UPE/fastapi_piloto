from fastapi import FastAPI
import random as rd

app = FastAPI()

@app.get("/")
def home():
    return {"Olá" : "Mundo!"}

@app.get("/aleatorio/{limite}")
def numero_aleatorio(limite : int):
    num = rd.randint(0, limite)
    return {"Número" : num}

vendas = {
    1: {"item": "lata", "preco_unitario": 4, "quantidade": 5},
    2: {"item": "garrafa 2L", "preco_unitario": 15, "quantidade": 5},
    3: {"item": "garrafa 750ml", "preco_unitario": 10, "quantidade": 5},
    4: {"item": "lata mini", "preco_unitario": 2, "quantidade": 5},
}


@app.get("/vendas/{id_venda}")
def pegar_venda(id_venda: int):
    if id_venda in vendas:
        return vendas[id_venda]
    else:
        return {"Erro": "ID Venda inexistente"}