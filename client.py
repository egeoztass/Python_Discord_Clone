import socket
import threading
from tkinter import messagebox


class DiSUcordClient:
    def __init__(self, server_ip='localhost', server_port=12345):
        self.subscribed_channels = set()
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
            self.running = True
            threading.Thread(target=self.receive_messages).start()
            return True
        except Exception as e:
            print(f"Failed to connect to the server: {e}")
            return False

    def disconnect_from_server(self):
        self.running = False
        if self.client_socket:
            self.client_socket.close()
        if self.message_callback:
            self.message_callback("Disconnected from server.")

    def on_connection_lost(self):
        self.running = False
        if self.message_callback:
            self.message_callback("Server closed the connection.")
        self.disconnect_from_server()

    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024)
                if len(message) == 0:
                    self.on_connection_lost()  # Server connection closed
                    break
                decoded_message = message.decode('utf-8')
                if self.message_callback:
                    self.message_callback(decoded_message)
            except socket.error as e:
                self.on_connection_lost()  # Socket error, likely disconnection
                break

    def send_channel_message(self, channel, message):
        if not self.running or channel not in self.subscribed_channels:
            messagebox.showerror("Error", "You are not properly connected or subscribed.")
            return

        formatted_message = f"{channel}:{message}"  # Include channel for server processing
        try:
            self.client_socket.send(formatted_message.encode('utf-8'))
        except Exception as e:
            # Handle errors here
            print(f"Error sending message: {e}")

    def send_message(self, message):
        try:
            self.client_socket.send(message.encode('utf-8'))
        except BrokenPipeError:
            messagebox.showerror("Connection Error", "Connection lost. Please reconnect.")
            self.disconnect_from_server()
        except Exception as e:
            print(f"Error sending message: {e}")

    def close_connection(self):
        self.running = False
        self.client_socket.close()

    def set_message_callback(self, callback):
        self.message_callback = callback

    def subscribe_to_channel(self, channel):
        if channel in self.subscribed_channels:
            messagebox.showinfo("Subscription", f"You are already subscribed to {channel}")
            return

        self.send_message(f"subscribe:{channel}")
        self.subscribed_channels.add(channel)

    def unsubscribe_from_channel(self, channel):
        if channel not in self.subscribed_channels:
            messagebox.showinfo("Unsubscription", f"You are not subscribed to {channel}")
            return

        self.send_message(f"unsubscribe:{channel}")
        self.subscribed_channels.discard(channel)
