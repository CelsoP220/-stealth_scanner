# sub_scanner.py
# ------------------------------------------------------------
# Módulo para varreduras de subdomínios.
# Monta URLs baseadas em subdomínios e testa se estão ativos.
# ------------------------------------------------------------

import requests
from concurrent.futures import ThreadPoolExecutor

# Verifica se o subdomínio está ativo
def verificar_subdominio(url_base, subdominio):
    subdominio = subdominio.strip()
    dominio = url_base.replace("https://", "").replace("http://", "").strip("/")
    full_url = f"http://{subdominio}.{dominio}"
    try:
        response = requests.get(full_url, timeout=3)
        if response.status_code < 400:
            print(f"[+] Subdomínio ativo: {full_url}")
            return full_url
    except requests.RequestException:
        pass
    return None

# Função principal

def scan(url, wordlist_path):
    with open (wordlist_path, 'r') as file:
        subdominios = file.readlines()

    resultados = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(verificar_subdominio, url, sub): sub for sub in subdominios}
        for future in futures:
            resultado = future.result()
            if resultado:
                resultados.append(resultado)

    return resultados