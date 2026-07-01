from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_BANCO_DE_DADOS = 'postgresql://postgres:1234@localhost:5432/Gerenciausuario'

caminho = create_engine(URL_BANCO_DE_DADOS)

SessaoLocal = sessionmaker(autocommit=False, autoflush=False, bind=caminho)

Base = declarative_base()