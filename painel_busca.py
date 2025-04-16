
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Painel de Busca de Parentes", layout="centered")

st.title("🔎 Painel de Busca de Parentes")

st.markdown("Preencha os dados abaixo para gerar links de busca e histórico.")

with st.form("form_busca"):
    nome_completo = st.text_input("Nome completo")
    rg = st.text_input("RG")
    cpf = st.text_input("CPF")
    celular = st.text_input("Celular")
    cidade = st.text_input("Cidade")
    sobrenome = st.text_input("Sobrenome (para busca reversa)")
    submitted = st.form_submit_button("Buscar")

st.markdown("## 📂 Histórico de Buscas")
if "historico" not in st.session_state:
    st.session_state.historico = []

if submitted:
    entrada = {
        "Nome": nome_completo,
        "RG": rg,
        "CPF": cpf,
        "Celular": celular,
        "Cidade": cidade,
        "Sobrenome": sobrenome,
    }
    st.session_state.historico.append(entrada)

if st.session_state.historico:
    df = pd.DataFrame(st.session_state.historico)
    st.dataframe(df, use_container_width=True)

    if st.button("🧹 Limpar Histórico"):
        st.session_state.historico = []
        st.experimental_rerun()

st.markdown("## 🌐 Buscas Diretas (Google e Redes Sociais)")
if nome_completo:
    nome_url = "+".join(nome_completo.split())
    google_url = f"https://www.google.com/search?q={nome_url}"
    fb_url = f"https://www.facebook.com/search/top/?q={nome_url}"
    ig_url = f"https://www.instagram.com/{nome_url.lower().replace(' ', '')}"
    twitter_url = f"https://twitter.com/search?q={nome_url}"

    st.markdown(f"[🔎 Google]({google_url})", unsafe_allow_html=True)
    st.markdown(f"[📘 Facebook]({fb_url})", unsafe_allow_html=True)
    st.markdown(f"[📸 Instagram]({ig_url})", unsafe_allow_html=True)
    st.markdown(f"[🐦 Twitter]({twitter_url})", unsafe_allow_html=True)

st.markdown("## 🔁 Busca Reversa por Sobrenome e Cidade")
if sobrenome or cidade:
    termo = f"{sobrenome} {cidade}".strip().replace(" ", "+")
    url = f"https://www.google.com/search?q={termo}"
    st.markdown(f"Buscar por sobrenome + cidade no Google: [{url}]({url})", unsafe_allow_html=True)

st.markdown("## 🧾 Upload de Documentos Antigos")
st.file_uploader("Envie certidões, fotos ou outros documentos antigos (formato PDF, JPG, PNG)", type=["pdf", "jpg", "jpeg", "png"])

st.markdown("## 🏢 Empresas Onde a Pessoa Pode Ter Trabalhado")
if nome_completo:
    nome_encoded = "+".join(nome_completo.split())
    linkedin_url = f"https://www.linkedin.com/search/results/people/?keywords={nome_encoded}"
    escavador_url = f"https://www.escavador.com/busca?q={nome_encoded}"
    google_empresas_url = f"https://www.google.com/search?q=%22{nome_encoded}%22+trabalhou+em"

    st.markdown("**Buscar no LinkedIn:**")
    st.markdown(f"[{linkedin_url}]({linkedin_url})", unsafe_allow_html=True)

    st.markdown("**Buscar no Escavador:**")
    st.markdown(f"[{escavador_url}]({escavador_url})", unsafe_allow_html=True)

    st.markdown("**Buscar no Google por empresas onde trabalhou:**")
    st.markdown(f"[{google_empresas_url}]({google_empresas_url})", unsafe_allow_html=True)
