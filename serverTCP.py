import socket
import os
import _thread as thread
import queue

tcp_ip = "127.0.0.1"
tcp_port = 8421
FILES_DIR = "ficheiros/"


def worker(conn):
    files = os.listdir(FILES_DIR)
    lista = ""
    for i, value in enumerate(files):
        lista += str(i) + " - " + value + "\n"
    print(files)
    conn.send("File list\n".encode('utf-8'))
    while 1:
        try:
            print("-----")
            conn.send(lista.encode('utf-8'))
            resp = conn.recv(64)
            sendFile(int(resp.decode('utf-8')), files, conn)
        except:
            break
    print("Client disconnected")


def main():
    print("File Sharing\n")
    q = queue.Queue()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((tcp_ip, tcp_port))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        print("Addr: " + str(addr))
        t = thread.start_new_thread(worker, (conn,))
        q.put(t)


def sendFile(identificador, files, conn):
    if identificador < 0 or identificador > len(files) - 1:
        conn.send("error".encode("utf-8"))
        return
    conn.send("accepted".encode("utf-8"))
    conn.send(files[identificador].encode("utf-8"))
    file_path = FILES_DIR + files[identificador]
    print("Sending file: " + file_path)
    file = open(file_path, "rb")

    block = file.read(1024)
    while (block):
        conn.send(block)
        block = file.read(1024)

    file.close()
    # sinalizar fim do arquivo
    # conn.send("end".encode("utf-8"))
    print("Ficheiro enviado")


if __name__ == '__main__':
    main()
