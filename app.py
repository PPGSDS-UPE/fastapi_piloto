import streamlit as st
import requests as rq
import random as rd

API_URL = "http://127.0.0.1:8000/usuarios"
API_URL_USUARIO="http://127.0.0.1:8000/usuario"

st.title("Gerenciamento de Usuário")

def carregar_usuarios():
    try:
        resposta = rq.get(API_URL)
        return resposta.json() if resposta.status_code == 200 else []
    except:
        return []

def atualizar_usuario(usuario_id, dados):
    resposta = rq.put(f"{API_URL_USUARIO}/{usuario_id}", json=dados)
    return resposta

def excluir_usuario(usuario_id):
    resposta = rq.delete(f"{API_URL_USUARIO}/{usuario_id}")
    return resposta

def adicionar_usuario(dados):
    dados["id"] = rd.randint(100, 9999)
    resposta = rq.post(f"{API_URL_USUARIO}", json=dados)
    return resposta

usuarios = carregar_usuarios()
#print(usuarios)
if usuarios:
    for indice, u in enumerate(usuarios):
        with st.expander(f"{u['nome']} ({u['cidade']})"):
            st.write("**Nome:**", u["nome"])
            st.write("**Idade:**", u["idade"])
            st.write("**Cidade:**", u["cidade"])
            st.write("**Senha:**", u["senha"])

            col1, col2 = st.columns(2)

            if col1.button("Editar", key=f"btn_editar{u['id']}"):
                st.session_state["editar_usuario"] = u
                st.rerun()

            if col2.button("Excluir", key=f"btn_excluir{u['id']}"):
                excluir_usuario(u["id"])
                st.rerun()

if "editar_usuario" in st.session_state:
    usuario = st.session_state["editar_usuario"]

    st.subheader(f"Editar Usuário: {usuario['nome']}")

    nome = st.text_input("Nome", usuario['nome'])
    idade = st.number_input("Idade", usuario['idade'])
    cidade = st.text_input("Cidade", usuario['cidade'])
    senha = st.text_input("Senha", usuario['senha'])

    if st.button("Atualizar Usuário"):
        dados = {
            "nome": nome,
            "idade": idade,
            "cidade": cidade,
            "senha": senha
        }
        atualizar_usuario(usuario["id"], dados)
        del st.session_state["editar_usuario"]
        st.success("Usuário atualizado!")
        st.rerun()

st.subheader("Adicionar Novo Usuário")

with st.form("add_usuario_form"):
    nome = st.text_input("Name")
    idade = st.number_input("Idade", min_value=1)
    cidade = st.text_input("Cidade")
    senha = st.text_input("Senha")

    enviar = st.form_submit_button("Adicionar Usuário")

    if enviar:
        dados = {
            "nome": nome,
            "idade": idade,
            "cidade": cidade,
            "senha": senha
        }
        adicionar_usuario(dados)
        st.success("Usuário Adicionado!")
        st.rerun()