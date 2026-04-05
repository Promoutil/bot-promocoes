import requests
from bs4 import BeautifulSoup
import re

URL = "https://meli.la/2xe3Uw2"

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("🔎 Acessando lista...")

r = requests.get(URL, headers=headers, allow_redirects=True)
html = r.text

# 🔥 pega IDs tipo MLB123456
ids = list(set(re.findall(r"MLB\d+", html)))

print(f"Produtos encontrados: {len(ids)}")

def get_produto(item_id):
    url = f"https://api.mercadolibre.com/items/{item_id}"
    return requests.get(url).json()

def formatar(prod):
    titulo = prod.get("title")
    preco = prod.get("price")
    original = prod.get("original_price")
    link = prod.get("permalink")

    if not titulo or not preco:
        return None

    desconto = 0
    if original:
        desconto = int((original - preco) / original * 100)

    # 🔥 filtro inteligente
    if desconto < 30:
        return None

    msg = f"""🔥 SUPER OFERTA

🛍️ {titulo}
💰 De R$ {original} por R$ {preco} ({desconto}% OFF)

👉 {link}

⚡ Corre que acaba!
"""
    return msg

mensagens = []

for item in ids:
    try:
        p = get_produto(item)
        msg = formatar(p)
        if msg:
            mensagens.append(msg)
    except:
        pass

print("Promoções boas:", len(mensagens))

with open("promocoes.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(mensagens))

print("✅ Arquivo pronto para WhatsApp!")
