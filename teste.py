import requests
import json
from googletrans import Translator
import datetime

def codigo2():
    # Inicializa o tradutor
    tradutor = Translator()

    API_KEY = "fe195371e4c2cb5bdae6cb82c7be3a49e3615e2b"
    URL_API = "https://findwork.dev/api/jobs/"

    # ------------------------------- #
    #   FUNÇÕES PRINCIPAIS DO SISTEMA
    # ------------------------------- #

    def traduzir_texto(texto, origem="en", destino="pt"):
        """Traduz qualquer texto usando googletrans."""
        try:
            traducao = tradutor.translate(texto, src=origem, dest=destino)
            return traducao.text
        except Exception:
            return "Erro ao traduzir texto."


    def buscar_vagas(area, local):
        """Busca vagas na API pública e retorna os dados."""
        try:
            params = {"search": area_en, "location": local_en}
            headers = {"Authorization": f"Token {API_KEY}"}

            resposta = requests.get(URL_API, headers=headers, params=params)

            if resposta.status_code != 200:
                print("⚠️ Erro ao acessar a API.")
                return None

            return resposta.json()

        except requests.exceptions.RequestException:
            print("⚠️ Erro de conexão.")
            return None


    def exibir_vagas(vagas):
        """Mostra as vagas traduzidas no terminal."""
        if not vagas or not vagas.get("results"):
            print("⚠️ Nenhuma vaga encontrada.")
            return

        for job in vagas["results"]:
            print("=" * 80)
            print(f"📌 Título: {job['role']}")
            print(f"🏢 Empresa: {job['company_name']}")
            print(f"📍 Local: {job['location']}")
            print(f"🔗 Link: {job['url']}")
            print("-" * 80)

            descricao = job.get("text", "")
            descricao = descricao[:4500]  # evitar limites do Google Translate

            descricao_traduzida = traduzir_texto(descricao)

            print("📝 Descrição traduzida:")
            print(descricao_traduzida[:200] + "...")
            print("=" * 80)


    def salvar_historico(area, local, vagas):
        """Salva o resultado da busca em arquivo JSON."""
        dados = {
            "area": area,
            "local": local,
            "data_busca": str(datetime.datetime.now()),
            "vagas": vagas
        }

        try:
            with open("historico_buscas.json", "a", encoding="utf-8") as file:
                file.write(json.dumps(dados, ensure_ascii=False, indent=4))
                file.write(",\n")

            print("💾 Histórico salvo com sucesso!")
        except:
            print("⚠️ Erro ao salvar histórico.")


    def mostrar_menu():
        """Menu principal do sistema."""
        print("\n===== BRIDGELY – BUSCADOR DE VAGAS =====")
        print("1 - Buscar vagas")
        print("2 - Ver histórico gravado")
        print("3 - Sair")
        return input("Escolha uma opção: ")


    def mostrar_historico():
        """Mostra o conteúdo salvo no JSON."""
        try:
            with open("historico_buscas.json", "r", encoding="utf-8") as file:
                conteudo = file.read()
                print("\n===== HISTÓRICO =====")
                print(conteudo)
        except:
            print("⚠️ Nenhum histórico encontrado.")


    # ------------------------------- #
    #            PROGRAMA
    # ------------------------------- #

    while True:
        opcao = mostrar_menu()

        if opcao == "1":
            area = input("Digite a área de tecnologia desejada: ").strip()
            local = input("Digite sua localização: ").strip()

            if area == "" or local == "":
                print("⚠️ Os campos não podem ficar vazios.")
                continue

            # Traduz a área para buscar em inglês
            area_en = traduzir_texto(area, origem="pt", destino="en")
            local_en = traduzir_texto(local, origem="pt", destino="en")

            print(f"\n🔍 Buscando vagas para '{area_en}' em '{local_en}'...\n")

            vagas = buscar_vagas(area_en, local_en)

            exibir_vagas(vagas)

            # salvar no histórico
            salvar_historico(area, local, vagas)

        elif opcao == "2":
            mostrar_historico()

        elif opcao == "3":
            print("Encerrando o programa. Até logo!")
            break

        else:
            print("⚠️ Opção inválida. Tente novamente.")
