import streamlit as st
import urllib.parse
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import pdfkit

def gerar_links_busca(nome, cidade):
    query_base = f"{nome} {cidade}".strip()
    query_encoded = urllib.parse.quote_plus(query_base)
    return {
        "Google Redes Sociais": f"https://www.google.com/search?q={query_encoded}+site:facebook.com+OR+site:linkedin.com+OR+site:instagram.com",
        "FamilySearch": f"https://www.familysearch.org/search/?q={query_encoded}",
        "MyHeritage": f"https://www.myheritage.com.br/names?s={query_encoded}",
    }

def buscar_no_google(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    resultados = []
    for resultado in soup.select("div.g"):
        titulo_tag = resultado.find("h3")
        link_tag = resultado.find("a")
        if titulo_tag and link_tag:
            resultados.append({
                "titulo": titulo_tag.text,
                "link": link_tag['href']
            })
    return resultados

st.title("🔎 Painel de Busca de Parentes em Lote")
st.markdown("Cole abaixo uma lista de **nomes completos**, um por linha:")

nomes_texto = st.text_area("Lista de nomes", value="Eduardo Zucco Paoli\nMaria Aparecida Silva")
cidade = st.text_input("Cidade (opcional)", value="Camboriú SC")

resultados_gerais = []

if st.button("Buscar todos"):
    nomes = [nome.strip() for nome in nomes_texto.split('\n') if nome.strip()]
    for nome in nomes:
        st.markdown(f"### 🔍 Resultados para: **{nome}**")
        resultados = buscar_no_google(f"{nome} {cidade} site:facebook.com OR site:linkedin.com OR site:instagram.com")
        if resultados:
            for item in resultados:
                st.markdown(f"🔗 [{item['titulo']}]({item['link']})")
                resultados_gerais.append({
                    "Nome": nome,
                    "Título": item["titulo"],
                    "Link": item["link"]
                })
        else:
            st.info(f"Nenhum resultado automático encontrado para **{nome}**.")
        st.markdown("#### 🌐 Links úteis:")
        links = gerar_links_busca(nome, cidade)
        for label, url in links.items():
            st.markdown(f"- [{label}]({url})", unsafe_allow_html=True)
        st.markdown("---")

    if resultados_gerais:
        df = pd.DataFrame(resultados_gerais)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue().encode('utf-8')
        st.download_button("📥 Baixar resultados em CSV", data=csv_bytes, file_name="resultados_busca_parentes.csv", mime="text/csv")

        html_string = df.to_html(index=False)
        pdfkit.from_string(html_string, "resultados_busca_parentes.pdf")
        with open("resultados_busca_parentes.pdf", "rb") as f:
            st.download_button("📄 Baixar resultados em PDF", data=f, file_name="resultados_busca_parentes.pdf", mime="application/pdf")

st.markdown("---")
st.subheader("🔄 Busca Reversa por Sobrenome + Cidade")
sobrenome = st.text_input("Sobrenome (ex: Paoli)")
cidade_reversa = st.text_input("Cidade", value="Camboriú SC")

if st.button("Buscar por sobrenome"):
    termo = f"{sobrenome} {cidade_reversa} site:facebook.com OR site:linkedin.com OR site:instagram.com"
    st.markdown(f"### Resultados para sobrenome: **{sobrenome}**, cidade: **{cidade_reversa}**")
    resultados = buscar_no_google(termo)
    if resultados:
        for item in resultados:
            st.markdown(f"🔗 [{item['titulo']}]({item['link']})")
    else:
        st.info("Nenhum resultado encontrado com esse sobrenome.")
