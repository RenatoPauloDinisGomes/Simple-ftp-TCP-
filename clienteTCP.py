import socket
import os
import sys

tcp_ip = "127.0.0.1"
tcp_port = 8421
DIR_PATH = "ficheiros_cliente/"


def main():
    print("Cliente file transfer")
    s = socket.socket()
    s.connect((tcp_ip, tcp_port))
    print("Connected\n")
    data = s.recv(1024)
    print(data.decode("utf-8"))
    while 1:
        # receber list files
        data = s.recv(1024)
        print(data.decode("utf-8"))
        data = input("file: ")
        # enviar index do ficheiro escolhido
        s.send(data.encode("utf-8"))
        # resposta
        res = s.recv(1024).decode("utf-8")

        if res == "error":
            print("Error")
        elif res == "accepted":
            # receber nome ficheiro
            try:
                nome = s.recv(1024).decode("utf-8")
            except:
                nome = "noname"
                print("Unable to get name")
            # receber ficheiro
            file = open(DIR_PATH + nome, "wb")

            i = 0
            while True:
                block = s.recv(1024)
                print(sys.getsizeof(block))
                if len(block) == 1024:
                    file.write(block)
                else:
                    #lastblock
                    file.write(block)
                    break

            file.close()

            print("Ficheiro recebido")
        else:
            print("Ups ????")


if __name__ == '__main__':
    main()
