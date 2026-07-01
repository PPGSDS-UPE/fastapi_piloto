from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from bd import Base

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    idade = Column(Integer, nullable=False)
    cidade = Column(String, nullable=False)
    senha = Column(String, nullable=False)