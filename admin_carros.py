import socket

from config import SERVIDOR_HOST, SERVIDOR_PORTA

def iniciar_conexao():
    host = input("Digite o IP do servidor: ")
    porta = int(input("Digite a porta do servidor: "))

    # Validação dos valores com o servidor
    if host != SERVIDOR_HOST or porta != SERVIDOR_PORTA:
        print("Erro: IP ou porta inválidos. Conexão recusada.")
        exit(1)

    return host, porta

def menu_admin(host, porta):
    while True:
        print("\n=== Menu do Admin ===")
        print("1. Adicionar novo carro")
        print("2. Deletar carro")
        print("3. Listar carros registrados")
        print("4. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            adicionar_carro(host, porta)
        elif escolha == "2":
            deletar_carro(host, porta)
        elif escolha == "3":
            listar_carros(host, porta)
        elif escolha == "4":
            print("Encerrando admin...")
            break
        else:
            print("Opção inválida! Tente novamente.")

def adicionar_carro(host, porta):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as admin:
            admin.connect((host, porta))
            marca = input("Digite a marca do carro: ")
            modelo = input("Digite o modelo do carro: ")
            ano = input("Digite o ano do carro: ")
            cor = input("Digite a cor do carro: ")

            carro = f"{marca},{modelo},{ano},{cor}"
            admin.sendall(f"ADICIONAR_CARRO|{carro}".encode())

            resposta = admin.recv(1024).decode()
            print("\n", resposta)
    except ConnectionRefusedError:
        print("Erro: Não foi possível conectar ao servidor.")

def deletar_carro(host, porta):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as admin:
            admin.connect((host, porta))
            admin.sendall("LISTAR_CARROS".encode())
            resposta = admin.recv(4096).decode()

            if "Nenhum carro disponível" in resposta:
                print("Não há carros para deletar.")
                return

            print("\n=== Carros Disponíveis ===")
            print(resposta)
            index = input("Digite o número do carro que deseja deletar: ")

            admin.sendall(f"DELETAR_CARRO|{index}".encode())
            resposta_deletar = admin.recv(1024).decode()
            print("\n", resposta_deletar)
    except ConnectionRefusedError:
        print("Erro: Não foi possível conectar ao servidor.")

def listar_carros(host, porta):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as admin:
            admin.connect((host, porta))
            admin.sendall("LISTAR_CARROS".encode())
            resposta = admin.recv(4096).decode()

            print("\n=== Carros Disponíveis ===")
            print(resposta)
    except ConnectionRefusedError:
        print("Erro: Não foi possível conectar ao servidor.")

if __name__ == "__main__":
    host, porta = iniciar_conexao()
    menu_admin(host, porta)