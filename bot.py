print("📥 Lendo lista de produtos...")

with open("produtos.txt", "r") as f:
    links = [l.strip() for l in f.readlines() if l.strip()]

print(f"🔗 Produtos carregados: {len(links)}")

mensagens = []

for link in links:
    mensagens.append(f"""🔥 *OFERTA IMPERDÍVEL* 🔥

👉 {link}

""")

with open("promocoes.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(mensagens))

print("✅ Arquivo pronto para WhatsApp!")
