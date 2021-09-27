import socket
import threading

class SocketUtils:

    @staticmethod
    def connect(socket, ip, port):
        try:
            socket.connect((ip, port))
            return True
        except Exception as e:
            print("Unable to connnect.")
            print(e)
            return False

    @staticmethod
    def send_message(socket, message):
        socket.send(message.encode())

    @staticmethod
    def send_bytes(socket, message):
        final_message = bytearray(message)
        final_message.extend(b'\xac')
        socket.send(final_message)

    @staticmethod
    def read_bytes(sock):
        buff = bytearray()
        while True:
            character = sock.recv(1)
            if character == b'\xac':
                break
            buff.extend(bytearray(character))
        return buff

    @staticmethod
    def read_message(sock):
        buff = ""
        while True:
            character = sock.recv(1).decode()
            if character == '\0':
                break
            buff += character
        return buff

