import requests
import re

# 🔗 seus links afiliados (meli.la)
LINKS = [
    "https://meli.la/2zCvW4r",
    "https://meli.la/11dVZRZ",
    "https://meli.la/2UqPKkk",
    "https://meli.la/2aYAQiX",
    "https://meli.la/2f7eTm3"
]

headers = {
    "User-Agent": "Mozilla/5.0"
}


# 🔍 descobre link real
def expandir_link(url):
    try:
        r = requests.get(url, headers=headers, allow_redirects=True)
        return r.url
    except:
        return None


# 🔍 extrai ID do produto
def extrair_id(url):
    match = re.search(r"MLB-?(\d+)", url)
    if match:
        return f"MLB{match.group(1)}"
    return None


# 🔍 busca produto na API
def get_produto(item_id):
    try:
        url = f"https://api.mercadolibre.com/items/{item_id}"
        r = requests.get(url)
        return r.json()
    except:
        return None


mensagens = []

print("🔎 Processando links...")

for link in LINKS:
    print(f"➡️ Link: {link}")

    real = expandir_link(link)
    if not real:
        print("❌ Não expandiu")
        continue

    item_id = extrair_id(real)
    if not item_id:
        print("❌ Não achou ID")
        continue

    produto = get_produto(item_id)
    if not produto or "title" not in produto:
        print("❌ Produto inválido")
        continue

    titulo = produto.get("title")
    preco = produto.get("price")

    # 🔥 usa SEU link afiliado original
    mensagem = f"""🔥 *OFERTA* 🔥

🛍️ {titulo}
💰 R$ {preco}

👉 {link}

"""

    mensagens.append(mensagem)


print(f"✅ Produtos processados: {len(mensagens)}")


# garante que não fica vazio
if not mensagens:
    mensagens.append("⚠️ Nenhum produto encontrado.")


# 💾 salva arquivo
with open("promocoes.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(mensagens))


print("📁 Arquivo pronto para WhatsApp!")
