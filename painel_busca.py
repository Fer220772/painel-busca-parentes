import streamlit as st
import pandas as pd
import base64
import graphviz
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Painel Completo de Busca de Parentes", layout="wide")
st.title("🔍 Painel Completo de Busca de Parentes")

if "buscas" not in st.session_state:
    st.session_state["buscas"] = []

# ENTRADAS
col1, col2 = st.columns(2)
with col1:
    nome = st.text_input("Nome completo", "")
    rg = st.text_input("RG", "")
    cpf = st.text_input("CPF", "")
with col2:
    celular = st.text_input("Celular", "")
    cidade = st.text_input("Cidade", "")

# Variações de nome
def gerar_variacoes(nome):
    partes = nome.strip().split()
    variacoes = set()
    if len(partes) >= 2:
        variacoes.add(f"{partes[0]} {partes[-1]}")
        variacoes.add(f"{partes[0][0]}. {partes[-1]}")
        variacoes.add(f"{partes[-1]}, {partes[0]}")
    variacoes.add(nome.upper())
    return list(variacoes)

# Simula busca
def buscar_registros(nome, cidade):
    sobrenome = nome.strip().split()[-1] if nome else "Sobrenome"
    return [
        {"Nome": nome or "João " + sobrenome, "CPF": "000.000.000-00", "RG": "1.111.111", "Celular": "(47) 99999-0000", "Cidade": cidade or "Exemplo"},
        {"Nome": "Maria " + sobrenome, "CPF": "111.111.111-11", "RG": "2.222.222", "Celular": "(47) 98888-0000", "Cidade": cidade or "Exemplo"},
    ]

# BOTÃO BUSCAR
if st.button("🔎 Buscar pessoa"):
    variacoes = gerar_variacoes(nome)
    resultados = buscar_registros(nome, cidade)
    df = pd.DataFrame(resultados)
    st.session_state["buscas"].append({"nome": nome, "cidade": cidade})
    st.subheader("📋 Resultados encontrados:")
    st.dataframe(df)

    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    st.markdown(f"📥 [Baixar CSV](data:file/csv;base64,{b64})", unsafe_allow_html=True)

    st.markdown("🧠 **Variações sugeridas:**")
    st.write(", ".join(variacoes))

# ÁRVORE GENEALÓGICA
st.markdown("---")
st.subheader("🌳 Árvore Genealógica Visual")
dot = graphviz.Digraph()
dot.node("A", "Bisavô João")
dot.node("B", "Avô Carlos")
dot.node("C", "Pai Eduardo")
dot.node("D", nome if nome else "Você")
dot.edges(["AB", "BC", "CD"])
st.graphviz_chart(dot)

# MAPA DE SOBRENOME
st.markdown("---")
st.subheader("🗺️ Mapa de Distribuição")
m = folium.Map(location=[-27.0, -48.6], zoom_start=6)
sobrenome = nome.split()[-1] if nome else "Silva"
folium.Marker(location=[-27.0, -48.6], tooltip=f"{sobrenome} - {cidade or 'Local'}").add_to(m)
st_folium(m, width=700)

# UPLOAD DOCUMENTOS
st.markdown("---")
st.subheader("📂 Upload de Documentos Antigos")
upload = st.file_uploader("Envie fotos ou PDFs antigos (certidões, imagens)", type=["png", "jpg", "jpeg", "pdf"])
if upload:
    st.success(f"Arquivo {upload.name} enviado com sucesso!")

# HISTÓRICO
st.markdown("---")
st.subheader("📌 Histórico de buscas")
if st.session_state["buscas"]:
    hist_df = pd.DataFrame(st.session_state["buscas"])
    st.dataframe(hist_df)
else:
    st.info("Nenhuma busca realizada ainda.")