#Scanner.py
#----------------------------------------------------------------------
#Ferramenta de varredura de diretórios e subdomínios
#Desenvolvida por Celso P.
#Descrição: este scripit recebe argumentos via terminal e executa
#           uma varredura em diretorios ou subdomínios utilizando
#           listas de palavras (Wordlists) e executando as requisições
#           em paralelo para melhorar a performace.
#----------------------------------------------------------------------

import argparse #Para receber argumentos via terminal
import os #para verificar caminhos e criar diretorios
from modules import dir_scanner, sub_scanner #Modulos customizados

# ---------------------------
#   Logo
# ---------------------------

def print_banner():
    banner = """
                        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⣛⣛⣛⣛⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣉⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣶⣮⡙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                        ⣿⣿⣿⣿⠛⠉⢉⠉⡙⣿⣿⣿⣿⣿⣿⣿⢁⣿⣿⣿⡿⠟⣿⣿⣿⣿⣿⣿⣿⣟⡛⠿⣿⣿⣇⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                        ⣿⣿⣿⣇⢰⣾⠟⢛⣁⠹⣿⣿⣿⣿⣿⡇⢸⡟⣩⠁⠒⠿⢿⣿⣿⣿⣿⣿⣿⠿⠟⠃⢈⡉⢿⡄⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                        ⣿⣿⣿⣿⡆⠀⣴⣷⠖⡀⢻⣿⣿⣿⣿⠁⣿⠀⣿⣿⣶⣶⣥⣄⣀⣉⣁⣀⣤⡴⣶⣾⣿⣷⢸⣧⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                        ⣿⣿⣿⣿⣷⡐⠶⣠⣤⠍⡈⢿⣿⣿⣿⢀⣿⡄⠻⢿⣿⣿⣿⣿⡿⢋⣽⠿⣋⣼⣿⣿⡿⠏⣸⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                        ⣿⣿⣿⣿⣿⣧⢰⡭⢉⣘⡓⠘⣿⣿⣿⢸⣿⡇⢰⣶⠈⠉⠍⣛⡛⠉⠐⢚⣋⠉⠉⠱⣶⡄⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                        ⣿⣿⣿⣿⣿⣿⣄⢈⣉⠛⠰⠦⢹⣿⣿⢸⣿⡇⢹⣿⣮⡹⠖⢀⠩⠿⠏⢉⡐⠾⢋⣼⣿⠇⢻⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                        ⣿⣿⣿⣿⣿⣿⣿⡘⣁⡚⠏⠠⠆⢻⣿⠘⣿⠃⣧⡙⠟⣋⣤⣴⣶⣶⣶⣶⣤⣌⡛⠿⢋⡄⢸⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                        ⣿⣿⣿⣿⣿⣿⣿⣧⠸⠃⠴⠖⢰⠌⣿⡄⢿⡇⢋⣥⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣌⠃⢸⠉⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                        ⣿⣿⣿⣿⣿⣿⣿⣿⣇⠛⡁⠞⠁⠂⠈⡃⢸⡀⢻⣿⣿⣿⣿⣟⠻⢿⡿⢿⣿⣿⣿⣿⣿⡇⣸⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                        ⣿⣿⣿⣿⣿⣿⣿⡿⠿⠀⣀⠬⠴⢚⠀⣠⡈⣧⠀⠹⣿⣿⣿⣿⣿⣶⣶⣿⣿⣿⣿⣿⠏⢀⡿⢰⡌⢙⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                        ⣿⣿⣿⣿⣿⡿⠋⠐⠾⠟⠀⣾⣿⣿⣄⢻⣿⣿⣇⠱⡘⢿⣿⣿⣿⣿⣿⡏⠀⠈⠿⠃⠔⣼⣿⣿⠇⣸⣿⣿⣦⠙⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                        ⣿⣿⣿⡏⣡⠲⢲⣶⣶⠀⡆⢿⣿⣿⣿⣎⢻⣿⣿⣷⣌⡂⠙⠿⣿⣿⡏⠀⠀⠠⠀⣪⣴⣿⣿⢏⣼⣿⣿⣿⠃⣼⣿⣶⡶⠒⣂⡉⣿⣿⣿⣿⣿⣿⣿⣿
                        ⣿⣿⣿⡗⢈⣴⣦⡈⢿⣆⠁⠘⣿⣿⣿⣿⣷⣙⠻⣿⣿⣿⣿⣷⣶⣶⠀⠁⣾⠃⢸⣿⣿⢟⣡⣾⣿⣿⣿⠇⣰⣿⣿⠟⢡⣶⣄⠁⢿⣿⣿⣿⣿⣿⣿⣿
                        ⣿⣿⡏⢠⣿⣿⣿⣿⡄⢻⡈⣦⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢰⢰⣿⣷⢸⣿⣿⣿⣿⣿⣿⣿⠋⣰⣿⣿⡟⢠⣿⣿⣿⣧⠈⣿⣿⣿⣿⣿⣿⣿
                        ⣿⣿⠁⢸⣿⣿⣿⣿⣿⡀⢧⠸⣦⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡎⣾⣯⣍⢸⡿⢿⣿⣿⣿⣿⠃⣼⣿⣿⡿⢁⣿⣿⣿⣿⣿⡆⠘⣿⣿⣿⣿⣿⣿
                        ⣿⡟⠀⢸⣿⣿⣿⣿⣿⠗⢸⣇⢻⣷⣄⠙⢿⣿⣿⣿⣿⣿⣿⣿⡿⢰⣧⠿⠿⠿⢠⣶⠀⣿⣿⡟⢡⣾⣿⣿⣿⠇⠼⣿⣿⣿⣿⣿⣧⢰⡘⣿⣿⣿⣿⣿
                        ⣿⠀⣿⡄⢿⣿⠟⣫⣤⣶⣄⠻⣆⢻⣿⣷⣦⣉⡛⠿⢿⣿⣿⡿⠀⠠⢄⠈⣤⣤⣴⡶⠶⠄⢩⣴⣿⣿⣿⣿⢿⢰⡶⣠⣙⠿⣿⣿⣿⡘⣷⠸⣿⣿⣿⣿
                        ⡇⣼⣿⣷⠈⣷⡾⢻⣿⣿⣿⣧⡙⣧⠙⣿⣿⣿⣿⣷⣔⠒⠂⣠⣾⣷⡌⣷⢸⣿⣿⣿⣷⣶⣦⠈⣿⣿⣿⣿⡇⢂⣼⣿⣿⣷⢿⣿⣿⣧⡘⢇⢹⣿⣿⣿
                        ⡇⣿⣿⣿⣾⣿⢡⣿⣿⣿⣿⣿⣧⠸⣷⡌⢿⣿⣿⣿⠟⠁⢳⠹⣿⣿⡇⣿⠘⠿⠆⣛⠉⢿⡿⠀⣿⣿⣿⣿⠁⣾⣿⣿⣿⣿⠸⣿⣿⣿⣷⣷⡆⢿⣿⣿
                        ⡇⣿⢿⣿⣿⡇⣾⣿⡿⠟⢛⣉⣭⣤⣾⣶⣶⣶⣶⣶⣾⣷⠀⣧⡙⡿⢡⡏⠸⢿⡆⢘⠻⠖⢂⣼⣿⣿⣿⡇⣼⣿⣿⣿⣿⣿⡇⢹⣿⣿⣿⣯⢻⠘⣿⣿
                        ⡇⢿⠸⣿⣿⡇⠙⢡⡄⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣷⡈⢷⣄⠻⠁⣾⡶⢀⣾⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⡿⠟⢸⣿⣿⣿⣿⣆⠄⣿⣿
                        ⣿⠸⡇⣿⡿⠋⠀⢸⣧⢹⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⣡⣾⣿⣷⣤⠙⠀⢀⣭⡐⠿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠸⣿⠿⠛⢋⡀⢶⣦⡉⠻⠿⢿⣿⣆⢻⣿
                        ⣿⣧⠁⢸⡇⣰⣿⠘⣿⡄⢿⣿⣿⣿⠿⠟⣉⣥⣶⣿⣿⣿⣿⣿⠟⢡⣾⣿⣿⣿⣦⣌⠻⣿⣿⣿⣿⣿⣿⡿⢀⣵⣾⣿⣿⣿⡎⢻⣷⠘⣶⣬⡻⣿⡘⣿
                        ⣿⣿⡆⢸⡇⣿⣿⣇⠸⣿⡌⢿⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⡿⢃⣀⢉⡡⠤⠤⠬⠭⠁⠉⠀⠍⠙⠛⣛⣥⣾⣿⣿⣿⣿⣿⣿⣿⡌⣿⡇⢹⣿⣿⣿⡀⢹
                        ⣿⣿⡇⢸⣿⣿⣿⣿⣦⠈⢿⣦⠹⣿⣿⣿⣿⣿⣿⡿⠟⢁⠴⣾⢁⠎⣴⣾⣿⣿⣿⣷⣦⠑⡈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢻⣧⢸⣿⣿⣿⡇⢸
                        ⣿⣿⣷⡀⢿⣿⣿⣿⣿⣷⡌⠻⣷⣎⠙⢿⠿⢟⣩⣴⢂⣤⡾⠁⢸⢸⣿⣿⣿⣿⣿⣿⣿⡇⢰⠈⣿⣏⣙⣛⡛⠛⠿⠛⣛⣋⣩⣽⢸⣿⢸⣿⣿⡿⢁⣾
                        ⣿⣿⣿⣧⣄⡙⠻⠿⠿⠿⠿⠷⠀⣙⣛⣀⣾⣿⣿⠃⢘⣫⡤⡀⢸⠸⣿⣿⣿⣿⣿⣿⣿⣿⢸⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⣿⢸⣿⠟⣠⣾⣿
                        ⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⠀⠟⣋⣴⡿⠘⢇⠙⠿⠿⠿⠿⠿⠟⠃⠸⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⣸⡏⣨⣴⣾⣿⣿⣿
                        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠸⢿⣿⣧⣦⠄⢉⣒⣒⣒⣂⣠⣭⣤⣤⣶⣶⣮⣭⣭⣭⣭⣭⣭⣭⣴⣶⣦⣭⣶⣿⣿⣿⣿⣿⣿
                        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠹⢹⢇⣔⡶⣤⡤⠤⠿⠿⢿⣿⣿⣽⣍⢭⢿⡿⢩⣭⢭⣿⣹⢭⣬⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    """
    print(banner)

# ---------------------------
# Função principal
# ---------------------------

def main():
    #criação do parser de argumentos
    parser = argparse.ArgumentParser(description="Scanner de Diretórios e Subdomínios")

    #Argumento obrigatório: URL base
    parser.add_argument('-u', '--url', required=True, help='URL do alvo (ex: https://exemplo.com)')

    #Tipo de varredura: subdomínios ou diretórios
    parser.add_argument('-m', '--mode', required=True, choices=['sub', 'dir'],
                        help='Modo de varredura: "sub" para subdomínios ou "dir" para diretórios')
    #caminho para a wordlist
    parser.add_argument('-w', '--wordlist', required=True, help='Caminho para a wordlist (ex: /caminho/para/wordlist.txt)')

    #Nome do arquivo de saída
    parser.add_argument('-o', '--output', default='results/output.txt', help='Arquivo para salvar)')

    args = parser.parse_args() #Faz o parse dos argumentos passados via terminal

    # Verifica a existencia da wordlist
    if not os.path.exists(args.wordlist):
        print(f'[!] Wordlist não encontrada: {args.wordlist}')
        return
    
    #Cria a pasta de resultados, se não existir
    os.makedirs('results', exist_ok=True)

    #Execução baseada no modo escolhido
    # Execução baseada no modo escolhido
    if args.mode == 'dir':
        print_banner()
        print('[*] Iniciando varredura de diretórios...')
        resultados = dir_scanner.scan(args.url, args.wordlist)

    elif args.mode == 'sub':
        print_banner()
        print('[*] Iniciando varredura de subdomínios...')
        resultados = sub_scanner.scan(args.url, args.wordlist)

    else:
        print('[!] Modo inválido.')

    with open (args.output, 'w') as f:
            for linha in resultados:
                f.write(linha + '\n')
            print (f'[+] Varredura concluida. Resultados salvos em: {args.output}')

# ---------------------------
# Execução direta do script
# ---------------------------

if __name__ == '__main__':
    main()