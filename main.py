from fastapi import FastAPI, Request, Response, status, HTTPException
#import random as rd

app = FastAPI()

usuarios = [{
    "id": 1,
    "nome": "Pedro",
    "idade": 25,
    "cidade": "Serra Talhada",
    "senha": "abc123"
}]

@app.get("/")
def apresentar_app():
    return {"Mensagem" : "Aplicação simples com CRUD FastAPI!"}

#Pegar usuários
@app.get("/usuarios")
def pegar_usuarios():
    return usuarios

@app.post("/usuario")
async def criar_usuario(request : Request, response: Response):
    usuario = await request.json()
    response.status_code = status.HTTP_201_CREATED
    usuarios.append(usuario)
    #print(usuarios)
    return {
        "dados retornados" : usuarios
    }

@app.get("/usuario/{usuario_id}")
async def pegar_usuario_por_id(usuario_id : int, response : Response):
    for indice, usuario in enumerate(usuarios):
        if usuario["id"] == usuario_id:
            response.status_code = status.HTTP_200_OK
            return usuarios[indice]


@app.put("/usuario/{usuario_id}")
async def atualizar_usuario(usuario_id : int, request : Request, response : Response):
    usuario_json = await request.json()
    for indice, usuario in enumerate(usuarios):
        if usuario["id"] == usuario_id:
            usuarios[indice].update(usuario_json)
            response.status_code = status.HTTP_200_OK
    return{
        "dados retornados" : usuarios[indice]
    }


@app.delete("/usuario/{usuario_id}")
async def excluir_usuario(usuario_id : int, request : Request, response : Response):
    for indice, usuario in enumerate(usuarios):
        if usuario["id"] == usuario_id:
            del usuarios[indice]
            response.status_code = status.HTTP_204_NO_CONTENT
            return
    raise HTTPException(status_code=404, detail="Usuário não encontrado!")


















"""
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
    """