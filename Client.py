import socket
import threading

from Cipher import Vignere
from Network import SocketUtils
import rsa
import hashlib

class Client(threading.Thread):
    def __init__(self, remote_ip, remote_port):
        threading.Thread.__init__(self, name="Client")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        public_key, private_key = rsa.newkeys(512)
        self.public_key = public_key
        self.private_key = private_key
        self.server_symmetric_key = ""

    def run(self):
        if SocketUtils.connect(self.socket, self.remote_ip, self.remote_port):
            print("Enviando chave pública para servidor...")
            self.send_public_key()
            self.server_symmetric_key = self.read_server_symmetric_key()
            print("Chave simétrica do servidor: " + self.server_symmetric_key)

            while True:
                message = input("Digite sua mensagem para o servidor>")
                cyphertext = Vignere.encrypt(self.server_symmetric_key, message)
                print("Enviando texto cifrado: " + cyphertext)
                SocketUtils.send_message(self.socket, cyphertext + "\0")
                digital_signature = Vignere.encrypt(self.server_symmetric_key, hashlib.md5(cyphertext.encode()).hexdigest())
                print("Enviando assinatura digital da mensagem...")
                SocketUtils.send_message(self.socket, digital_signature + "\0")

    def send_public_key(self):
        SocketUtils.send_message(self.socket, self.public_key.save_pkcs1().decode('utf-8') + "\0")

    def read_server_symmetric_key(self):
        server_symmetric_key_encrypted = SocketUtils.read_bytes(self.socket)
        return rsa.decrypt(server_symmetric_key_encrypted, self.private_key).decode()

def main():
    remote_ip = input("Remote Ip:")
    remote_port = int(input("Remote Port:"))
    Client(remote_ip, remote_port).start()


if __name__ == "__main__":
    main()