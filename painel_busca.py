import streamlit as st
import pandas as pd
import base64
import graphviz
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Painel Genealógico Aprimorado", layout="wide")
st.title("🌐 Painel Genealógico Aprimorado")

# Histórico de buscas na sessão
if "buscas" not in st.session_state:
    st.session_state["buscas"] = []

# Entrada de dados
col1, col2 = st.columns(2)
with col1:
    nome_completo = st.text_input("Nome completo", "")
with col2:
    cidade = st.text_input("Cidade", "")

sobrenome = ""
if nome_completo:
    sobrenome = nome_completo.strip().split()[-1]

# Sugestão de variações
def gerar_variacoes(nome):
    partes = nome.strip().split()
    variacoes = set()
    if len(partes) >= 2:
        variacoes.add(f"{partes[0]} {partes[-1]}")
        variacoes.add(f"{partes[0][0]}. {partes[-1]}")
        variacoes.add(f"{partes[-1]}, {partes[0]}")
    variacoes.add(nome.upper())
    return list(variacoes)

# Busca simulada
def buscar_registros(sobrenome, cidade):
    resultados = [
        {"Nome": "Carlos " + sobrenome, "Cidade": cidade or "Exemplo", "Telefone": "(47) 90000-1234"},
        {"Nome": "Maria " + sobrenome, "Cidade": cidade or "Exemplo", "Telefone": "(47) 91111-5678"},
    ]
    return resultados

# Botão de busca
if st.button("Buscar"):
    variacoes = gerar_variacoes(nome_completo)
    resultados = buscar_registros(sobrenome, cidade)
    df = pd.DataFrame(resultados)
    st.session_state["buscas"].append({"nome": nome_completo, "cidade": cidade})
    st.subheader("Resultados encontrados:")
    st.dataframe(df)

    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    st.markdown(f"📥 [Baixar CSV](data:file/csv;base64,{b64})", unsafe_allow_html=True)

    st.markdown("📑 **Variações de nome sugeridas:**")
    st.write(", ".join(variacoes))

# Árvore Genealógica (exemplo estático)
st.markdown("---")
st.subheader("🌳 Árvore Genealógica Visual")
dot = graphviz.Digraph()
dot.node("A", "Bisavô João")
dot.node("B", "Avô Carlos")
dot.node("C", "Pai Eduardo")
dot.node("D", nome_completo if nome_completo else "Você")
dot.edges(["AB", "BC", "CD"])
st.graphviz_chart(dot)

# Mapa de sobrenome
st.markdown("---")
st.subheader("🗺️ Distribuição do sobrenome")
m = folium.Map(location=[-27.0, -48.6], zoom_start=6)
folium.Marker(location=[-27.0, -48.6], tooltip=f"{sobrenome} - Camboriú").add_to(m)
st_data = st_folium(m, width=700)

# Upload de documentos
st.markdown("---")
st.subheader("📂 Upload de Documentos Antigos")
upload = st.file_uploader("Envie fotos ou PDFs de documentos antigos", type=["png", "jpg", "jpeg", "pdf"])
if upload:
    st.success(f"Arquivo {upload.name} enviado com sucesso!")

# Histórico
st.markdown("---")
st.subheader("📌 Histórico de buscas")
if st.session_state["buscas"]:
    hist_df = pd.DataFrame(st.session_state["buscas"])
    st.dataframe(hist_df)
else:
    st.info("Nenhuma busca realizada ainda.")