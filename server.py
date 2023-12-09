import socket
import threading

class DiSUcordServer:
    def __init__(self, host='localhost'):
        self.host = host
        self.port = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.channels = {"IF 100": set(), "SPS 101": set()}
        self.log_callback = None
        self.is_running = False
        self.threads = []

    def set_port(self, port):
        self.port = port

    def start(self):
        if self.port is None:
            raise ValueError("Port number not set.")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.is_running = True
        self.log(f"Server started on {self.host}:{self.port}")

        try:
            while self.is_running:
                self.server_socket.settimeout(1.0)
                try:
                    conn, addr = self.server_socket.accept()
                except socket.timeout:
                    continue
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
                self.threads.append(thread)
        except Exception as e:
            self.log(f"Server stopped with error: {e}")
        finally:
            self.server_socket.close()
            for thread in self.threads:
                thread.join()

    def stop(self):
        self.is_running = False
        self.log("Server is shutting down")
        for _, conn in self.clients.items():
            conn.close()

    def handle_client(self, conn, addr):
        try:
            username = conn.recv(1024).decode('utf-8')
            if username in self.clients:
                self.log(f"Username {username} already in use.")
                conn.send("Username already in use.".encode('utf-8'))
                conn.close()
                return

            self.clients[username] = conn
            self.log(f"{username} connected from {addr}")

            while True:
                message = conn.recv(1024).decode('utf-8')
                if message:
                    # Message format "channel:message"
                    channel, msg = message.split(':', 1)
                    if channel in self.channels and username in self.channels[channel]:
                        self.multicast_message(f"{username}: {msg}", channel)
                    else:
                        self.log(f"Message to an unsubscribed/unrecognized channel {channel} by {username}")
                else:
                    break
        except Exception as e:
            if self.is_running:  # Only log error if the server is supposed to be running
                self.log(f"Error with {username}: {e}")
        finally:
            conn.close()
            del self.clients[username]
            for channel in self.channels:
                self.channels[channel].discard(username)
            self.log(f"{username} has disconnected.")

    def multicast_message(self, message, channel):
        for username, conn in self.clients.items():
            if username in self.channels[channel]:
                try:
                    conn.send(message.encode('utf-8'))
                except Exception as e:
                    self.log(f"Error sending message to {username}: {e}")

    def set_log_callback(self, callback):
        self.log_callback = callback

    def log(self, message):
        if self.log_callback:
            self.log_callback(message)
