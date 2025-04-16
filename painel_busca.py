import streamlit as st
import pandas as pd
import base64
import urllib.parse

st.set_page_config(page_title="Painel de Busca de Parentes", layout="wide")
st.title("👨‍👩‍👧‍👦 Painel de Busca de Parentes")

# Histórico de buscas
if "buscas" not in st.session_state:
    st.session_state["buscas"] = []

# Entradas principais
with st.form("form_busca"):
    st.subheader("🔍 Parâmetros de busca")
    nome = st.text_input("Nome completo")
    rg = st.text_input("RG")
    cpf = st.text_input("CPF")
    celular = st.text_input("Celular")
    cidade = st.text_input("Cidade")
    sobrenome_busca = st.text_input("Busca reversa por sobrenome")
    submitted = st.form_submit_button("Buscar")

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
    sobrenome = nome.strip().split()[-1] if nome else "Silva"
    return [
        {"Nome": nome or "João " + sobrenome, "CPF": "000.000.000-00", "RG": "1.111.111", "Celular": "(47) 99999-0000", "Cidade": cidade or "Exemplo"},
        {"Nome": "Maria " + sobrenome, "CPF": "111.111.111-11", "RG": "2.222.222", "Celular": "(47) 98888-0000", "Cidade": cidade or "Exemplo"},
    ]

# Resultado
if submitted:
    resultados = buscar_registros(nome, cidade)
    df = pd.DataFrame(resultados)
    st.session_state["buscas"].append({
        "Nome": nome,
        "RG": rg,
        "CPF": cpf,
        "Celular": celular,
        "Cidade": cidade,
        "Sobrenome": sobrenome_busca
    })

    st.subheader("📋 Resultados encontrados:")
    st.dataframe(df)

    # Exportar CSV
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    st.markdown(f"📥 [Baixar CSV](data:file/csv;base64,{b64})", unsafe_allow_html=True)

    # Variações de nome
    st.markdown("🧠 **Variações de nome sugeridas:**")
    st.write(", ".join(gerar_variacoes(nome)))

    # Busca Google e redes sociais
    st.markdown("🌐 **Buscar online:**")
    query = urllib.parse.quote_plus(f"{nome} {cidade}")
    st.markdown(f"- [🔎 Google](https://www.google.com/search?q={query})", unsafe_allow_html=True)
    st.markdown(f"- [🔵 Facebook](https://www.facebook.com/search/top/?q={query})", unsafe_allow_html=True)
    st.markdown(f"- [📸 Instagram](https://www.instagram.com/{nome.replace(' ', '').lower()}/)", unsafe_allow_html=True)
    st.markdown(f"- [🐦 Twitter](https://twitter.com/search?q={query})", unsafe_allow_html=True)

# Upload de documentos
st.markdown("---")
st.subheader("📂 Upload de Documentos Antigos")
arquivo = st.file_uploader("Envie certidões, imagens ou PDFs antigos", type=["pdf", "png", "jpg", "jpeg"])
if arquivo:
    st.success(f"Arquivo '{arquivo.name}' enviado com sucesso!")

# Histórico de buscas
st.markdown("---")
st.subheader("📌 Histórico de buscas")
col_hist1, col_hist2 = st.columns([4,1])
with col_hist1:
    if st.session_state["buscas"]:
        st.dataframe(pd.DataFrame(st.session_state["buscas"]))
    else:
        st.info("Nenhuma busca realizada ainda.")
with col_hist2:
    if st.session_state["buscas"]:
        if st.button("🧹 Limpar histórico"):
            st.session_state["buscas"] = []
            st.experimental_rerun()