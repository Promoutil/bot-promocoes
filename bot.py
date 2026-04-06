import requests
from bs4 import BeautifulSoup
import re

# 🔗 Sua lista afiliada
URL = "https://meli.la/2xe3Uw2"

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("🔎 Acessando lista...")

# pega HTML da página
response = requests.get(URL, headers=headers, allow_redirects=True)
html = response.text

# 🔥 extrai IDs dos produtos (MLBxxxx)
ids = list(set(re.findall(r"MLB\d+", html)))

print(f"📦 Produtos encontrados: {len(ids)}")


# 🔎 função para buscar dados na API
def get_produto(item_id):
    url = f"https://api.mercadolibre.com/items/{item_id}"
    r = requests.get(url)
    return r.json()


# 🧠 função para montar mensagem
def formatar(prod):
    titulo = prod.get("title")
    preco = prod.get("price")
    original = prod.get("original_price")
    link = prod.get("permalink")

    if not titulo or not preco:
        return None

    # monta preço
    if original:
        desconto = int((original - preco) / original * 100)
        preco_texto = f"💰 De R$ {original} por R$ {preco} ({desconto}% OFF)"
    else:
        desconto = 0
        preco_texto = f"💰 R$ {preco}"

    # 🔥 REGRA NOVA (garante conteúdo)
    if preco > 200:
        return None

    msg = f"""🔥 *OFERTA DO DIA* 🔥

🛍️ {titulo}
{preco_texto}

👉 {link}

⚡ Corre que acaba!
"""
    return msg


# 🚀 processa produtos
mensagens = []

for item in ids:
    try:
        produto = get_produto(item)
        msg = formatar(produto)

        if msg:
            mensagens.append(msg)

    except Exception as e:
        print(f"Erro no item {item}: {e}")


print(f"🔥 Promoções boas: {len(mensagens)}")


# 💾 salva arquivo
with open("promocoes.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(mensagens))


print("✅ Arquivo pronto para WhatsApp!")
