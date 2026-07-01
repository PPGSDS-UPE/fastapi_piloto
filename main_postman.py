from fastapi import FastAPI, Request, Response, status, HTTPException

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
