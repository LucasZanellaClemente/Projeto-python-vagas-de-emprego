import json
import requests
import os
import time
from teste import codigo2


def codigo1():
    # ==============================================================================
    # CONSTANTES E CONFIGURAÇÕES
    # ==============================================================================
    ARQUIVO_DADOS = "dados_bridgely.json"
    URL_API_LIVROS = "https://openlibrary.org/search.json"

    CORES = {
        "limpa": "\033[0m",
        "vermelho": "\033[91m",
        "verde": "\033[92m",
        "amarelo": "\033[93m",
        "azul": "\033[94m",
        "ciano": "\033[96m",
        "negrito": "\033[1m"
    }

    # ==============================================================================
    # FUNÇÕES UTILITÁRIAS E DE INTERFACE
    # ==============================================================================


    def limpar_tela():
        """
        Limpa o buffer do terminal de acordo com o sistema operacional.
        """
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')


    def exibir_cabecalho():
        """
        Exibe o cabeçalho padrão do sistema com formatação ANSI.
        """
        print(CORES["ciano"] + CORES["negrito"])
        print("="*60)
        print("   F U T U R O   D O   T R A B A L H O   |   B R I D G E L Y  A I  2 0 2 5")
        print("="*60)
        print(f"\n   >>> SISTEMA INTEGRADO DE REQUALIFICAÇÃO <<<{CORES['limpa']}")
        print("-" * 60)


    def animacao_carregando(mensagem: str):
        """
        Exibe uma barra de progresso simulada para feedback visual.

        Args:
            mensagem (str): Texto a ser exibido durante o carregamento.
        """
        print(f"\n{CORES['amarelo']}⏳ {mensagem}...", end="", flush=True)
        for _ in range(3):
            time.sleep(0.3)
            print(".", end="", flush=True)
        print(f"{CORES['limpa']}")

    # ==============================================================================
    # CAMADA DE PERSISTÊNCIA (JSON)
    # ==============================================================================


    def carregar_dados() -> list:
        """
        Lê o arquivo JSON local e retorna a estrutura de dados.

        Returns:
            list: Lista de usuários e trilhas. Retorna lista vazia em caso de erro.
        """
        if not os.path.exists(ARQUIVO_DADOS):
            return []
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except (IOError, json.JSONDecodeError):
            return []


    def salvar_dados(dados: list) -> None:
        """
        Persiste a estrutura de dados no arquivo JSON local.

        Args:
            dados (list): A lista completa de usuários para salvar.
        """
        try:
            with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, indent=4, ensure_ascii=False)
            print(
                f"\n{CORES['verde']}💾 Registro atualizado com sucesso.{CORES['limpa']}")
            time.sleep(1.5)
        except IOError as e:
            print(f"{CORES['vermelho']}❌ Erro de I/O: {e}{CORES['limpa']}")

    # ==============================================================================
    # CAMADA DE INTEGRAÇÃO (API)
    # ==============================================================================


    def buscar_livros_educativos(tema: str) -> list:
        """
        Consulta a Open Library API para buscar livros técnicos.
        """
        animacao_carregando(f"Buscando referências para '{tema}'")

        params = {
            'q': tema,
            'limit': 3,
            'fields': 'title,author_name,first_publish_year'
        }

        try:
            response = requests.get(URL_API_LIVROS, params=params, timeout=10)
            response.raise_for_status()
            dados_api = response.json()

            livros_encontrados = []
            docs = dados_api.get("docs", [])

            if not docs:
                print(
                    f"\n{CORES['amarelo']}⚠️ A API retornou 0 livros.{CORES['limpa']}")
                return []

            for item in docs:
                titulo = item.get("title", "Título não informado")
                autores = item.get("author_name", ["Autor desconhecido"])
                autor = autores[0] if autores else "Autor desconhecido"
                # Tratamento para evitar erro se o ano não existir
                ano = str(item.get("first_publish_year", "N/A"))

                livros_encontrados.append({
                    "titulo": titulo,
                    "autor": autor,
                    "ano": ano
                })

            return livros_encontrados

        except requests.exceptions.RequestException as e:
            print(
                f"\n{CORES['vermelho']}❌ Erro de Conexão/API: {e}{CORES['limpa']}")
            return []
        except Exception as e:
            print(f"\n{CORES['vermelho']}❌ Erro genérico: {e}{CORES['limpa']}")
            return []

    # ==============================================================================
    # LÓGICA DE NEGÓCIO
    # ==============================================================================


    def buscar_indice_usuario(nome: str, dados: list) -> int:
        """
        Localiza o índice de um usuário na lista baseada no nome.

        Returns:
            int: Índice do usuário ou -1 se não encontrado.
        """
        indice = 0
        for usuario in dados:
            if usuario['nome'].lower() == nome.lower():
                return indice
            indice += 1
        return -1


    def adicionar_trilha(dados: list) -> None:
        """
        Fluxo de cadastro de usuário e criação de nova trilha de estudo.
        """
        limpar_tela()
        exibir_cabecalho()
        print(f"{CORES['negrito']}NOVA TRILHA DE APRENDIZADO{CORES['limpa']}")

        nome = input("Nome do Colaborador/Usuário: ").strip()
        if not nome:
            print(
                f"{CORES['vermelho']}⚠️ Erro: O nome é obrigatório.{CORES['limpa']}")
            input("Pressione ENTER para continuar...")
            return

        tema = input("Tema de interesse (ex: Liderança, Python): ").strip()
        if not tema:
            print(
                f"{CORES['vermelho']}⚠️ Erro: O tema é obrigatório.{CORES['limpa']}")
            input("Pressione ENTER para continuar...")
            return

        bibliografia = buscar_livros_educativos(tema)

        nova_trilha = {
            "tema": tema,
            "data_criacao": time.strftime("%d/%m/%Y"),
            "status": "Ativo",
            "recursos": bibliografia
        }

        indice = buscar_indice_usuario(nome, dados)

        if indice != -1:
            # Usuário existente: atualiza lista de trilhas
            print(
                f"\n{CORES['azul']}ℹ️ Usuário localizado. Atualizando perfil...{CORES['limpa']}")
            dados[indice]['trilhas'].append(nova_trilha)
        else:
            # Novo usuário: cria registro completo
            print(f"\n{CORES['azul']}ℹ️ Novo cadastro iniciado.{CORES['limpa']}")
            novo_usuario = {
                "nome": nome,
                "trilhas": [nova_trilha]
            }
            dados.append(novo_usuario)

        salvar_dados(dados)


    def consultar_usuario(dados: list) -> None:
        """
        Exibe o perfil completo e trilhas de um usuário específico.
        """
        limpar_tela()
        exibir_cabecalho()
        print(f"{CORES['negrito']}CONSULTA DE PERFIL{CORES['limpa']}")

        nome_busca = input("Pesquisar por nome: ").strip()
        indice = buscar_indice_usuario(nome_busca, dados)

        if indice == -1:
            print(
                f"\n{CORES['vermelho']}❌ Usuário não encontrado na base de dados.{CORES['limpa']}")
        else:
            usuario = dados[indice]
            print(
                f"\n{CORES['verde']}RESUMO DO PERFIL: {usuario['nome'].upper()}{CORES['limpa']}")
            print(f"Trilhas cadastradas: {len(usuario['trilhas'])}")

            for trilha in usuario['trilhas']:
                print(
                    f"\n   {CORES['amarelo']}📘 [{trilha['status']}] Tema: {trilha['tema']}{CORES['limpa']}")

                if not trilha['recursos']:
                    print("      (Nenhum recurso externo localizado)")

                for livro in trilha['recursos']:
                    print(
                        f"      • {livro['titulo']} ({livro['ano']}) - {livro['autor']}")
            print("_"*60)

        input("\nPressione ENTER para voltar ao menu...")


    def listar_geral(dados: list) -> None:
        """
        Exibe um relatório tabular de todos os usuários cadastrados.
        """
        limpar_tela()
        exibir_cabecalho()
        print(f"{CORES['negrito']}RELATÓRIO GERAL{CORES['limpa']}")

        if not dados:
            print(
                f"\n{CORES['amarelo']}Nenhum registro encontrado.{CORES['limpa']}")
        else:
            print(f"{'COLABORADOR':<30} | {'QTD TRILHAS':<10}")
            print("-" * 45)
            for usuario in dados:
                print(f"{usuario['nome']:<30} | {len(usuario['trilhas']):<10}")

        input("\nPressione ENTER para voltar ao menu...")

    # ==============================================================================
    # BLOCO PRINCIPAL
    # ==============================================================================


    def menu():
        """
        Controlador principal do fluxo de execução.
        """
        dados = carregar_dados()

        while True:
            limpar_tela()
            exibir_cabecalho()

            print("1. Adicionar Trilha / Novo Usuário")
            print("2. Consultar Perfil")
            print("3. Relatório Geral")
            print(f"{CORES['vermelho']}4. Encerrar{CORES['limpa']}")
            print("-" * 60)

            opcao = input(f"{CORES['negrito']}Opção: {CORES['limpa']}")

            if opcao == '1':
                adicionar_trilha(dados)
            elif opcao == '2':
                consultar_usuario(dados)
            elif opcao == '3':
                listar_geral(dados)
            elif opcao == '4':
                print(f"\n{CORES['azul']}Finalizando aplicação...{CORES['limpa']}")
                time.sleep(1)
                break
            else:
                print(f"\n{CORES['vermelho']}Opção inválida.{CORES['limpa']}")
                time.sleep(1)


    if __name__ == "__main__":
        menu()

def main():
    while True:
        print("\n===== SISTEMA BRIDGELY =====")
        print("1 - Buscar vagas (API de empregos)")
        print("2 - Criar trilha de estudos (OpenLibrary)")
        print("3 - Sair")

        opcao = input("Escolha: ")

        match opcao:
            case "1":
                codigo2()
            case "2":
                codigo1()
            case "3":
                print("Encerrando...")
                break
            case _:
                print("Opção inválida!")

if __name__ == "__main__":
    main()

