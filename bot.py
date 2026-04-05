import requests

# IDs dos produtos (você pode alimentar manualmente)
PRODUTOS = [
    "MLB123456789",
    "MLB987654321"
]

def get_produto(item_id):
    url = f"https://api.mercadolibre.com/items/{item_id}"
    r = requests.get(url)
    return r.json()

def montar_mensagem(prod):
    titulo = prod["title"]
    preco = prod["price"]
    link = prod["permalink"]

    msg = f"""🔥 PROMOÇÃO 🔥
{titulo}
💰 R$ {preco}

👉 {link}
"""
    return msg

mensagens = []

for item in PRODUTOS:
    try:
        produto = get_produto(item)
        mensagens.append(montar_mensagem(produto))
    except:
        pass

with open("promocoes.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(mensagens))

print("Arquivo gerado com sucesso!")
