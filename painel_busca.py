
import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import io

st.set_page_config(page_title="Painel de Busca de Parentes", layout="centered")

st.title("🔎 Painel de Busca de Parentes")

st.markdown("Preencha os dados abaixo para gerar links de busca, histórico e filtros avançados.")

with st.form("form_busca"):
    nome_completo = st.text_input("Nome completo")
    rg = st.text_input("RG")
    cpf = st.text_input("CPF")
    celular = st.text_input("Celular")
    cidade = st.text_input("Cidade onde morava")
    sobrenome = st.text_input("Sobrenome (para busca reversa)")
    cidade_empresa = st.text_input("Cidade da empresa (filtro avançado)")
    cargo_empresa = st.text_input("Cargo ou função (filtro avançado)")
    cnpj_empresa = st.text_input("CNPJ da empresa (opcional)")
    documento = st.file_uploader("📎 Envie certidões, fotos ou outros documentos antigos (PDF, JPG, PNG)", type=["pdf", "jpg", "jpeg", "png"])
    submitted = st.form_submit_button("Buscar")

# OCR de documento (se imagem)
ocr_text = ""
if documento and documento.type.startswith("image"):
    image = Image.open(documento)
    ocr_text = pytesseract.image_to_string(image)
    st.markdown("### 📄 Texto extraído do documento (OCR):")
    st.text_area("Resultado OCR", ocr_text, height=150)

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
        "Cidade Empresa": cidade_empresa,
        "Cargo": cargo_empresa,
        "CNPJ": cnpj_empresa
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

st.markdown("## 🏢 Empresas Onde a Pessoa Pode Ter Trabalhado")

if nome_completo:
    nome_encoded = "+".join(nome_completo.split())
    filtros = ""
    if cidade_empresa:
        filtros += f"+{cidade_empresa}"
    if cargo_empresa:
        filtros += f"+{cargo_empresa}"
    if cnpj_empresa:
        filtros += f"+{cnpj_empresa}"

    linkedin_url = f"https://www.linkedin.com/search/results/people/?keywords={nome_encoded}"
    escavador_url = f"https://www.escavador.com/busca?q={nome_encoded}"
    google_empresas_url = f"https://www.google.com/search?q=%22{nome_encoded}%22+trabalhou+em{filtros}"

    st.markdown("**Buscar no LinkedIn:**")
    st.markdown(f"[{linkedin_url}]({linkedin_url})", unsafe_allow_html=True)

    st.markdown("**Buscar no Escavador:**")
    st.markdown(f"[{escavador_url}]({escavador_url})", unsafe_allow_html=True)

    st.markdown("**Buscar no Google com filtros de empresa:**")
    st.markdown(f"[{google_empresas_url}]({google_empresas_url})", unsafe_allow_html=True)
