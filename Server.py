import hashlib
import socket
import threading

from Cipher import Vignere
from Network import SocketUtils
import rsa

symmetric_key = "chavesimetricadoservidor"

class Connection(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self, name="Connection")
        self.socket = socket
        self.client_pub_key = ""

    def run(self):
        self.client_pub_key = self.read_client_pub_key()
        print("Chave pública de cliente recebida. Enviando chave simétrica encriptada...")
        self.send_symmetric_key()

        while True:
            received_message = SocketUtils.read_message(self.socket)
            plain_text = Vignere.decrypt(symmetric_key, received_message)
            print("Mensagem recebida\n - Cifrada: " + received_message + "\n - Texto pleno: " + plain_text)

            digital_signature = SocketUtils.read_message(self.socket)
            print("Assinatura digital: " + digital_signature)
            decrypted_signature = Vignere.decrypt(symmetric_key, digital_signature)
            print("Assinatura digital decriptada: " + decrypted_signature)
            received_message_hash = hashlib.md5(received_message.encode()).hexdigest()
            print("Hash mensagem recebida: ", )

            if (received_message_hash == decrypted_signature):
                print("Assinatura digital validada!")
            else:
                print("Assinatura digital não validada")
i

    def read_client_pub_key(self):
        client_pub_key_text =  SocketUtils.read_message(self.socket)
        return rsa.PublicKey.load_pkcs1(client_pub_key_text)

    def send_symmetric_key(self):
        symmetric_key_encrypted = rsa.encrypt(symmetric_key.encode(), self.client_pub_key)
        print(symmetric_key_encrypted)
        SocketUtils.send_bytes(self.socket, symmetric_key_encrypted)

class Server(threading.Thread):
    def __init__(self,local_ip, local_port):
        threading.Thread.__init__(self, name="Server")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.local_ip = local_ip
        self.local_port = local_port
        self.connections = []

    def run(self):
        self.socket.bind((self.local_ip, self.local_port))
        self.socket.listen(16)

        while True:
            connection, client_address = self.socket.accept()
            self.connections.append(Connection(connection).start())

def main():
    local_ip = input("Local Ip:")
    local_port = int(input("Local Port:"))
    Server(local_ip, local_port).start()


if __name__ == "__main__":
    main()