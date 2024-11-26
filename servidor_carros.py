import socket
import threading

carros = [{"marca": "Toyota", "modelo": "Corolla", "ano": "2020", "cor": "Preto"}]

def gerenciar_cliente(conexao, endereco):
    print(f"Conexão estabelecida com {endereco}")

    while True:
        try:
            mensagem = conexao.recv(1024).decode()

            if not mensagem:
                break

            if mensagem == "LISTAR_CARROS":
                if carros:
                    resposta = "\n".join(
                        [f"{index+1}. {c['marca']} {c['modelo']} ({c['ano']}) - Cor: {c['cor']}" for index, c in enumerate(carros)]
                    )
                else:
                    resposta = "Nenhum carro disponível"
                conexao.sendall(resposta.encode())

            elif mensagem.startswith("ADICIONAR_CARRO|"):
                dados = mensagem.split("|")[1]
                marca, modelo, ano, cor = dados.split(",")
                carros.append({"marca": marca, "modelo": modelo, "ano": ano, "cor": cor})
                conexao.sendall("Carro adicionado com sucesso".encode())

            elif mensagem.startswith("DELETAR_CARRO|"):
                try:
                    index = int(mensagem.split("|")[1]) - 1
                    if 0 <= index < len(carros):
                        carro_deletado = carros.pop(index)
                        conexao.sendall(f"Carro {carro_deletado['marca']} {carro_deletado['modelo']} deletado com sucesso".encode())
                    else:
                        conexao.sendall("Índice inválido!".encode())
                except ValueError:
                    conexao.sendall("Índice inválido!".encode())

        except Exception as e:
            print(f"Erro ao lidar com o cliente {endereco}: {e}")
            break

    print(f"Conexão encerrada com {endereco}")
    conexao.close()

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind(("localhost", 12345))
        servidor.listen(5)
        print("Servidor iniciado e aguardando conexões...")

        while True:
            conexao, endereco = servidor.accept()
            threading.Thread(target=gerenciar_cliente, args=(conexao, endereco)).start()

if __name__ == "__main__":
    iniciar_servidor()