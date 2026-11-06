from base_conhecimento import BaseConhecimento
from assistente import Assistente


def main():
    base = BaseConhecimento("data/base_conhecimento.json")
    if not base.carregar():
        print("Não foi possível iniciar sem a base de conhecimento.")
        return

    assistente = Assistente("Citizen Assist AI", base)
    print(f"=== {assistente.nome} ===")
    print("Orientações para pessoas idosas, com base em fontes oficiais.")
    print("Este assistente NÃO é um canal oficial e nunca pede dados pessoais.")

    while True:
        print("\nMenu principal:")
        print("  1 - Fazer uma pergunta")
        print("  2 - Navegar por categorias")
        print("  3 - Ver indicadores")
        print("  4 - Exportar atendimentos para CSV")
        print("  0 - Sair")
        opcao = assistente.ler_opcao("Escolha uma opção: ", 4)

        if opcao == 1:
            assistente.perguntar()
        elif opcao == 2:
            assistente.navegar()
        elif opcao == 3:
            assistente.indicadores()
        elif opcao == 4:
            assistente.exportar_csv()
        else:
            assistente.encerrar()
            assistente.indicadores()
            print("Até logo!")
            break


if __name__ == "__main__":
    main()