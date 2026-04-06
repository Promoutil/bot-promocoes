import requests
import re

URL = "https://meli.la/2xe3Uw2"

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("🔎 Acessando lista...")

response = requests.get(URL, headers=headers, allow_redirects=True)
html = response.text

# pega possíveis IDs
ids = list(set(re.findall(r"MLB\d+", html)))

print(f"📦 IDs encontrados: {len(ids)}")


def get_produto(item_id):
    try:
        url = f"https://api.mercadolibre.com/items/{item_id}"
        r = requests.get(url)
        data = r.json()

        # valida produto
        if "title" not in data:
            return None

        return data
    except:
        return None


def formatar(prod):
    titulo = prod.get("title")
    preco = prod.get("price")
    link = prod.get("permalink")

    if not titulo or not preco:
        return None

    return f"""🔥 *OFERTA* 🔥

🛍️ {titulo}
💰 R$ {preco}

👉 {link}

"""


mensagens = []

for item in ids:
    produto = get_produto(item)

    if produto:
        msg = formatar(produto)

        if msg:
            mensagens.append(msg)


print(f"🔥 Produtos válidos: {len(mensagens)}")


# 🚨 GARANTIA: nunca fica vazio
if not mensagens:
    mensagens.append("⚠️ Nenhuma promoção encontrada dessa vez.\nTente novamente mais tarde.")


with open("promocoes.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(mensagens))


print("✅ Arquivo gerado!")
