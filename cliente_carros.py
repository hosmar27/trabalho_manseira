import socket

def iniciar_conexao():
    host = input("Digite o IP do servidor: ")
    porta = int(input("Digite a porta do servidor: "))
    return host, porta

def menu_cliente(host, porta):
    while True:
        print("\n\n=== Menu do Cliente ===")
        print("1. Listar carros")
        print("2. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            listar_carros(host, porta)
        elif escolha == "2":
            print("Encerrando cliente...")
            break
        else:
            print("Opção inválida! Tente novamente.")

def listar_carros(host, porta):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((host, porta))
            cliente.sendall("LISTAR_CARROS".encode())
            resposta = cliente.recv(4096).decode()
            print("\n=== Lista de Carros Disponíveis ===")
            print(resposta)
    except ConnectionRefusedError:
        print("Erro: Não foi possível conectar ao servidor.")

if __name__ == "__main__":
    host, porta = iniciar_conexao()
    menu_cliente(host, porta)
