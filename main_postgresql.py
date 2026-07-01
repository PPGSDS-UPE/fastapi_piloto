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


@app.post("/usuario")
async def criar_usuario(usuario: Usuario, bd: bd_dependencias):
    bd_usuario = m.Usuario(nome=usuario.nome, idade=usuario.idade, cidade=usuario.cidade, senha=usuario.senha)
    bd.add(bd_usuario)
    bd.commit()
    bd.refresh(bd_usuario)