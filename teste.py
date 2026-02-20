import os
import time

# ==== Cores ANSI para terminal bonito ====
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"

def efeito_loading(texto, tempo=0.02):
    print(C.CYAN + texto + C.RESET, end="")
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(tempo)
    print()

def linha_separadora():
    print(C.DIM + "─" * 50 + C.RESET)

def mostrar_resultados_organizados(resultados):
    total = sum(len(v) for v in resultados.values())

    if total == 0:
        print(C.RED + "❌ Nenhum login encontrado." + C.RESET)
        return

    print(C.GREEN + f"\n✔ {total} login(s) encontrado(s):" + C.RESET)
    linha_separadora()

    for arquivo, itens in resultados.items():
        if not itens:
            continue
        print(C.YELLOW + f"{arquivo}:" + C.RESET)
        for login, senha in itens:
            print(f"  {C.GREEN}{login}{C.RESET} : {C.RED}{senha}{C.RESET}")
        linha_separadora()

def buscar_por_termo(termo):
    txt_files = [f for f in os.listdir() if f.lower().endswith(".txt")]

    if not txt_files:
        print(C.RED + "⚠ Não há arquivos .txt neste diretório." + C.RESET)
        return

    efeito_loading(f"🔎 Buscando por '{termo}' em todos os .txt")

    resultados = {f: [] for f in txt_files}

    for arquivo in txt_files:
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                linhas = f.read().splitlines()
        except Exception as e:
            print(C.RED + f"⚠ Erro ao ler {arquivo}: {e}" + C.RESET)
            continue

        for linha in linhas:
            partes = linha.strip().split(":")

            # Formatos possíveis:
            # site:url:login:senha  -> 4 partes
            # url:login:senha       -> 3 partes
            if len(partes) == 4:
                _, url, login, senha = partes
            elif len(partes) == 3:
                url, login, senha = partes
            else:
                continue

            if termo.lower() in url.lower():
                resultados[arquivo].append((login, senha))

    mostrar_resultados_organizados(resultados)

def main():
    print(C.MAGENTA + f"{'='*10} BUSCA TURBINADA {'='*10}" + C.RESET)
    print(
        C.CYAN
        + "Digite '/buscar <termo>' para procurar credenciais em todos os .txt."
        + C.RESET
    )
    print(C.CYAN + "Digite '/sair' para encerrar.\n" + C.RESET)

    while True:
        comando = input(C.BOLD + ">>> " + C.RESET).strip()

        if comando.startswith("/buscar "):
            termo = comando.replace("/buscar ", "").strip()
            buscar_por_termo(termo)

        elif comando == "/sair":
            print(C.YELLOW + "👋 Encerrando… Até mais!" + C.RESET)
            break

        else:
            print(C.RED + "⚠ Comando inválido! Use: /buscar <termo> ou /sair" + C.RESET)

if __name__ == "__main__":
    main()