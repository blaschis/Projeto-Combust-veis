import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO

# URL da página
url = "https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/levantamento-de-precos-de-combustiveis-ultimas-semanas-pesquisadas"

# Requisição HTML
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Seleciona os links desejados com "Preços médios semanais: Brasil, regiões, estados e municípios" e ano "2024"
links = []
for a_tag in soup.find_all("a", href=True):
    # Verifica se o texto do link é o desejado e contém o ano 2024
    if "Preços médios semanais: Brasil, regiões, estados e municípios" in a_tag.text and "2024" in a_tag["href"]:
        # Constrói a URL
        full_url = a_tag["href"] if a_tag["href"].startswith("http") else f"https://www.gov.br{a_tag['href']}"
        links.append(full_url)

# Lista para armazenar os DataFrames
dataframes = []

# Faz o download e processamento
for link in links:
    file_response = requests.get(link)
    xlsx_data = BytesIO(file_response.content)
    # Lê o arquivo em um DataFrame, removendo as 9 primeiras linhas e usando a 10ª como cabeçalho
    df = pd.read_excel(xlsx_data, skiprows=9, header=0) 
    dataframes.append(df)

# Concatena
final_df = pd.concat(dataframes, ignore_index=True)

print(final_df)

final_df.info()