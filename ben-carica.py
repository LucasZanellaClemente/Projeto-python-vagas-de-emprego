from teste import codigo2
from VersãoFinal import codigo1

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

