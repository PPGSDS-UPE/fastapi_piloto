from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated
import modelos as m
from bd import caminho, SessaoLocal
from sqlalchemy.orm import Session


app = FastAPI()
m.Base.metadata.create_all(bind=caminho)

class Usuario(BaseModel):
    nome: str
    idade: int
    cidade: str
    senha: str

def conectar_bd():
    bd = SessaoLocal()
    try:
        yield bd
    finally:
        bd.close()

bd_dependencias = Annotated[Session, Depends(conectar_bd)]

@app.get("/")
def apresentar_app():
    return {"Mensagem" : "Aplicação simples com CRUD FastAPI!"}

@app.post("/usuario")
async def criar_usuario(usuario: Usuario, bd: bd_dependencias):
    bd_usuario = m.Usuario(nome=usuario.nome, idade=usuario.idade, cidade=usuario.cidade, senha=usuario.senha)
    bd.add(bd_usuario)
    bd.commit()
    bd.refresh(bd_usuario)

@app.get("/usuario/{usuario_id}")
async def pegar_usuario_por_id(usuario_id: int, bd: bd_dependencias):
    resultado = bd.query(m.Usuario).filter(m.Usuario.id == usuario_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return resultado

@app.get("/usuarios")
def pegar_usuarios(bd: bd_dependencias):
    resultado = bd.query(m.Usuario).all()
    return resultado

@app.delete("/usuario/{usuario_id}")
async def excluir_usuario(usuario_id: int, bd: bd_dependencias):
    resultado =  bd.query(m.Usuario).filter(m.Usuario.id == usuario_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    bd.delete(resultado)
    bd.commit()
    return {"Usuário excluído"}

@app.put("/usuario/{usuario_id}")
async def atualizar_usuario(usuario_id : int, usuario: Usuario, bd: bd_dependencias):
    resultado = bd.query(m.Usuario).filter(m.Usuario.id == usuario_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    for campo, valor in usuario.dict().items():
        setattr(resultado, campo, valor)
        
    bd.commit()
    bd.refresh(resultado)
    return resultado