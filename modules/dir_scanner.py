#dir_scanner.py
#----------------------------------------------------
#Módulo para varredura de diretórios.
#Envia rquisições para caminhos baseados na wordlist.
#Se o status for 200, adiciona a lista de resultados.
#----------------------------------------------------

import requests # Para enviar as requisições HTTP
from concurrent.futures import ThreadPoolExecutor # Execução paralela

#Função que verifica se um diretorio existe
def verificar_diretorio(url, path):
    path = path.strip() #remove espaços e quebras de linha
    full_url = f"{url.rstrip('/')}/{path}" # Concatena a url com o diretório
    try:
        response = requests.get(full_url, timeout=3) # Tenta acessar a URL
        if response.status_code in [200,301,302]:
            print(f"[+] Encontrado: {full_url}")
            return full_url
    except requests.RequestException:
        pass
    return None # Se não for 200 ou der erro, não retorna nada

#Função principal que recebe a URL e wordlist
def scan(url, wordlist_path):
    with open(wordlist_path, 'r') as file:
        paths = file.readlines()
    
    resultados = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        # Roda todas as threads ao mesmo tempo
        future_to_path = {executor.submit(verificar_diretorio, url, path): path for path in paths}

        for future in future_to_path:
            resultado = future.result()
            if resultado:
                resultados.append(resultado)

    return resultados