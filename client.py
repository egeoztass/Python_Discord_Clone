import socket
import threading

class DiSUcordClient:
    def __init__(self, server_ip='localhost', server_port=12345):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.running = False
        self.message_callback = None

    def connect_to_server(self, username):
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            self.username = username
            self.client_socket.send(username.encode('utf-8'))
            return True
        except Exception as e:
            print(f"Failed to connect to the server: {e}")
            return False

    def disconnect_from_server(self):
        try:
            self.running = False
            if self.client_socket:
                self.client_socket.close()
            print("Disconnected from the server.")
        except Exception as e:
            print(f"Failed to disconnect from the server: {e}")

    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message and self.message_callback:
                    self.message_callback(message)
            except Exception as e:
                break

    def send_channel_message(self, channel, message):
        full_message = f"{channel}:{message}"
        self.send_message(full_message)

    def send_message(self, message):
        try:
            self.client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")

    def close_connection(self):
        self.running = False
        self.client_socket.close()

    def set_message_callback(self, callback):
        self.message_callback = callback
