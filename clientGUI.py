import tkinter as tk
from tkinter import scrolledtext, messagebox
from client import DiSUcordClient  # Ensure this matches your client module name

class ClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("DiSUcord Client")
        master.geometry("500x400")

        # Connection Frame
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

        # Channel Subscription Frame
        channel_frame = tk.Frame(master)
        channel_frame.grid(row=1, column=0, sticky="ew")
        self.subscribe_button = tk.Button(channel_frame, text="Subscribe", command=self.subscribe_to_channel)
        self.subscribe_button.grid(row=0, column=0)
        self.unsubscribe_button = tk.Button(channel_frame, text="Unsubscribe", command=self.unsubscribe_from_channel)
        self.unsubscribe_button.grid(row=0, column=1)

        # Message Composition Frame
        message_frame = tk.Frame(master)
        message_frame.grid(row=2, column=0, sticky="ew")
        self.message_entry = tk.Entry(message_frame)
        self.message_entry.grid(row=0, column=0, sticky="ew")
        self.send_button = tk.Button(message_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1)

        # Message Display Area
        self.messages = scrolledtext.ScrolledText(master, state='disabled')
        self.messages.grid(row=3, column=0, sticky="nsew")

        # Client Instance
        self.client = None

    def connect_to_server(self):
        server_ip = self.server_ip_entry.get()
        server_port = int(self.port_entry.get())
        username = self.username_entry.get()
        self.client = DiSUcordClient(server_ip, server_port)
        self.client.set_message_callback(self.update_messages)  # Set message callback
        if self.client.connect_to_server(username):
            messagebox.showinfo("Connection", "Successfully connected to the server")
            self.connect_button.config(state=tk.DISABLED)  # Disable the connect button after connecting
        else:
            messagebox.showerror("Connection", "Failed to connect to the server")

    def subscribe_to_channel(self):
        # Implement logic to subscribe to a channel
        pass

    def unsubscribe_from_channel(self):
        # Implement logic to unsubscribe from a channel
        pass

    def send_message(self):
        message = self.message_entry.get()
        self.client.send_message(message)
        self.message_entry.delete(0, tk.END)  # Clear the message field

    def update_messages(self, message):
        # Ensure GUI updates are done in the main thread
        self.master.after(0, self.thread_safe_update, message)

    def thread_safe_update(self, message):
        self.messages.config(state='normal')
        self.messages.insert(tk.END, message + "\n")
        self.messages.config(state='disabled')
        self.messages.see(tk.END)  # Auto-scroll to the bottom

# Create and run the client GUI
root = tk.Tk()
gui = ClientGUI(root)
root.mainloop()
