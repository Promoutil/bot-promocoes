from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

URL = "https://www.mercadolivre.com.br/social/novaazul"

print("🔎 Abrindo página...")

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

driver.get(URL)

time.sleep(5)

print("📜 Rolando página...")

# rola algumas vezes pra carregar produtos
for _ in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

links = []

print("🔗 Coletando links...")

# pega todos os links meli.la
elements = driver.find_elements(By.TAG_NAME, "a")

for el in elements:
    href = el.get_attribute("href")
    if href and "meli.la" in href:
        links.append(href)

# remove duplicados
links = list(set(links))

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

print("📁 Arquivo pronto!")
driver.quit()
