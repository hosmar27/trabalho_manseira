import socket

def meu_ip():
    return socket.gethostbyname(socket.gethostname())

if __name__ == "__main__":
    print(f"Seu IP é: {meu_ip()}")