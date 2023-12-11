import tkinter as tk
from tkinter import scrolledtext, messagebox
from client import DiSUcordClient

class ClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("DiSUcord Client")
        master.geometry("500x400")

        connection_frame = tk.Frame(master)
        connection_frame.grid(row=0, column=0, sticky="ew")

        tk.Label(connection_frame, text="Server IP:").grid(row=0, column=0)
        self.server_ip_entry = tk.Entry(connection_frame)
        self.server_ip_entry.grid(row=0, column=1)

        tk.Label(connection_frame, text="Port:").grid(row=1, column=0)
        self.port_entry = tk.Entry(connection_frame)
        self.port_entry.grid(row=1, column=1)

        tk.Label(connection_frame, text="Username:").grid(row=2, column=0)
        self.username_entry = tk.Entry(connection_frame)
        self.username_entry.grid(row=2, column=1)

        self.connect_button = tk.Button(connection_frame, text="Connect", command=self.connect_to_server)
        self.connect_button.grid(row=3, column=0, columnspan=2)

        self.disconnect_button = tk.Button(connection_frame, text="Disconnect", command=self.disconnect_from_server, state=tk.DISABLED)
        self.disconnect_button.grid(row=4, column=0, columnspan=2)

        self.messages = scrolledtext.ScrolledText(master, state='normal')
        self.messages.grid(row=4, column=0, sticky="nsew")

        message_frame = tk.Frame(master)
        message_frame.grid(row=5, column=0, sticky="ew")

        self.message_entry = tk.Entry(message_frame)
        self.message_entry.grid(row=0, column=0, sticky="ew")

        self.send_button = tk.Button(message_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1)

        self.client = None

    def connect_to_server(self):
        server_ip = self.server_ip_entry.get()
        server_port = int(self.port_entry.get())
        username = self.username_entry.get()
        self.client = DiSUcordClient(server_ip, server_port)

        if self.client.connect_to_server(username):
            self.connect_button.config(state=tk.DISABLED)
            self.disconnect_button.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Connection Error", "Failed to connect to the server")

    def disconnect_from_server(self):
        if self.client:
            self.client.disconnect_from_server()
            self.connect_button.config(state=tk.NORMAL)
            self.disconnect_button.config(state=tk.DISABLED)

    def send_message(self):
        channel = "IF 100"  # Replace with the actual channel selection logic
        message = self.message_entry.get()
        if message:
            self.client.send_channel_message(channel, message)
            self.message_entry.delete(0, tk.END)
            self.messages.config(state='normal')
            self.messages.insert(tk.END, f"You: {message}\n")
            self.messages.config(state='disabled')


# Create and run the client GUI
root = tk.Tk()
gui = ClientGUI(root)
root.mainloop()
