import requests
from bs4 import BeautifulSoup

url = "https://www.mercadolivre.com.br/ofertas"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

produtos = soup.find_all("li")

for produto in produtos[:10]:
    try:
        texto = produto.get_text(strip=True)
        if "R$" in texto:
            print("🔥 OFERTA")
            print(texto[:120])
            print("-" * 30)
    except:
        pass
