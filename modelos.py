from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from bd import Base

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    idade = Column(Integer, index=True)
    cidade = Column(String, index=True)
    senha = Column(String, index=True)