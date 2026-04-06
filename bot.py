from playwright.sync_api import sync_playwright

URL = "https://www.mercadolivre.com.br/social/novaazul"

print("🔎 Abrindo página...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(URL)
    page.wait_for_timeout(5000)

    print("📜 Rolando página...")

    for _ in range(5):
        page.mouse.wheel(0, 5000)
        page.wait_for_timeout(2000)

    print("🔗 Coletando links...")

    links = page.eval_on_selector_all(
        "a",
        "elements => elements.map(e => e.href)"
    )

    links = list(set([l for l in links if "meli.la" in l]))

    print(f"✅ Links encontrados: {len(links)}")

    mensagens = []

    for link in links:
        mensagens.append(f"""🔥 *OFERTA* 🔥

👉 {link}

""")

    if not mensagens:
        mensagens.append("⚠️ Nenhum produto encontrado.")

    with open("promocoes.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(mensagens))

    browser.close()

print("📁 Arquivo pronto!")
