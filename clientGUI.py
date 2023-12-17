import tkinter as tk
from tkinter import scrolledtext, messagebox
from client import DiSUcordClient


class ClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("DiSUcord Client")
        master.geometry("800x700")

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

        self.disconnect_button = tk.Button(connection_frame, text="Disconnect", command=self.disconnect_from_server,
                                           state=tk.DISABLED)
        self.disconnect_button.grid(row=4, column=0, columnspan=2)

        # self.messages = scrolledtext.ScrolledText(master, state='normal')
        # self.messages.grid(row=4, column=0, sticky="nsew")

        message_frame = tk.Frame(master)
        message_frame.grid(row=5, column=0, sticky="ew")

        self.message_entry = tk.Entry(message_frame)
        self.message_entry.grid(row=0, column=0, sticky="ew")

        # Subscription Frame
        subscription_frame = tk.Frame(master)
        subscription_frame.grid(row=1, column=0, sticky="ew")

        # IF 100 Subscription Buttons
        self.subscribe_if100_button = tk.Button(subscription_frame, text="Subscribe to IF 100",
                                                command=self.subscribe_to_if100)
        self.subscribe_if100_button.grid(row=0, column=0)
        self.unsubscribe_if100_button = tk.Button(subscription_frame, text="Unsubscribe from IF 100",
                                                  command=self.unsubscribe_from_if100)
        self.unsubscribe_if100_button.grid(row=0, column=1)

        # SPS 101 Subscription Buttons
        self.subscribe_sps101_button = tk.Button(subscription_frame, text="Subscribe to SPS 101",
                                                 command=self.subscribe_to_sps101)
        self.subscribe_sps101_button.grid(row=1, column=0)
        self.unsubscribe_sps101_button = tk.Button(subscription_frame, text="Unsubscribe from SPS 101",
                                                   command=self.unsubscribe_from_sps101)
        self.unsubscribe_sps101_button.grid(row=1, column=1)

        # Status messages frame
        self.status_messages = scrolledtext.ScrolledText(master, state='disabled', height=4)
        self.status_messages.grid(row=2, column=0, sticky="nsew")

        # IF 100 Message Frame
        self.if100_message_entry = tk.Entry(master)
        self.if100_message_entry.grid(row=3, column=0, sticky="ew")
        self.send_if100_button = tk.Button(master, text="Send to IF 100",
                                           command=lambda: self.send_message("IF 100", self.if100_message_entry))
        self.send_if100_button.grid(row=3, column=1)

        self.if100_messages = scrolledtext.ScrolledText(master, state='disabled', height=8)
        self.if100_messages.grid(row=4, column=0, columnspan=2, sticky="nsew")

        # SPS 101 Message Frame
        self.sps101_message_entry = tk.Entry(master)
        self.sps101_message_entry.grid(row=5, column=0, sticky="ew")
        self.send_sps101_button = tk.Button(master, text="Send to SPS 101",
                                            command=lambda: self.send_message("SPS 101", self.sps101_message_entry))
        self.send_sps101_button.grid(row=5, column=1)

        self.sps101_messages = scrolledtext.ScrolledText(master, state='disabled', height=8)
        self.sps101_messages.grid(row=6, column=0, columnspan=2, sticky="nsew")

        self.client = None

        # Bind the clean-up function to the window close event
        master.protocol("WM_DELETE_WINDOW", self.on_close)

    def connect_to_server(self):
        server_ip = self.server_ip_entry.get()
        server_port = self.port_entry.get()
        username = self.username_entry.get()

        # Check for empty fields
        if not server_ip or not server_port or not username:
            messagebox.showwarning("Warning", "Please fill all the fields!")
            return

        # Check for valid port number
        try:
            server_port = int(server_port)
        except ValueError:
            messagebox.showerror("Error", "Invalid port number!")
            return

        self.client = DiSUcordClient(server_ip, server_port)

        try:
            if self.client.connect_to_server(username):
                self.client.set_message_callback(self.message_callback)  # Set the message callback
                self.connect_button.config(state=tk.DISABLED)
                self.disconnect_button.config(state=tk.NORMAL)
                self.enable_subscription_buttons()  # Enable subscription buttons upon successful connection
                self.update_status(f"Connected to {server_ip}:{server_port} as {username}")
            else:
                messagebox.showerror("Connection Error",
                                     "Failed to connect to the server. Make sure the server is running and the "
                                     "IP/Port is correct.")
        except BrokenPipeError:
            messagebox.showerror("Connection Error", "Cannot connect to the server. The server may not be running.")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")

    def enable_subscription_buttons(self):
        # Enable the subscription buttons
        self.subscribe_if100_button.config(state=tk.NORMAL)
        self.unsubscribe_if100_button.config(state=tk.NORMAL)
        self.subscribe_sps101_button.config(state=tk.NORMAL)
        self.unsubscribe_sps101_button.config(state=tk.NORMAL)

    def disable_subscription_buttons(self):
        # Disable the subscription buttons
        self.subscribe_if100_button.config(state=tk.DISABLED)
        self.unsubscribe_if100_button.config(state=tk.DISABLED)
        self.subscribe_sps101_button.config(state=tk.DISABLED)
        self.unsubscribe_sps101_button.config(state=tk.DISABLED)

    def disconnect_from_server(self):
        if self.client:
            self.client.disconnect_from_server()
            self.connect_button.config(state=tk.NORMAL)
            self.disconnect_button.config(state=tk.DISABLED)

    def send_message(self, channel_name, message_entry_widget):
        # Check if the user is subscribed to the channel
        if channel_name not in self.client.subscribed_channels:
            messagebox.showerror("Error", f"You are not subscribed to {channel_name}.")
            return

        # Get the message from the correct entry widget
        message = message_entry_widget.get()
        if message:
            self.client.send_channel_message(channel_name, message)
            message_entry_widget.delete(0, tk.END)  # Clear the entry widget after sending

    def subscribe_to_if100(self):
        if not self.client.running:
            self.update_status_message("You must be connected to the server to subscribe.")
            return
        if "IF 100" in self.client.subscribed_channels:
            self.update_status_message("You are already subscribed to IF 100.")
            return
        self.client.subscribe_to_channel("IF 100")
        self.client.subscribed_channels.add("IF 100")
        self.update_status_message("You are now subscribed to IF 100.")

    def unsubscribe_from_if100(self):
        if not self.client.running:
            self.update_status_message("You must be connected to the server to unsubscribe.")
            return
        if "IF 100" not in self.client.subscribed_channels:
            self.update_status_message("You are not subscribed to IF 100.")
            return
        self.client.unsubscribe_from_channel("IF 100")
        self.client.subscribed_channels.discard("IF 100")
        self.update_status_message("You are now unsubscribed from IF 100.")

    def subscribe_to_sps101(self):
        if not self.client.running:
            self.update_status_message("You must be connected to the server to subscribe.")
            return
        if "SPS 101" in self.client.subscribed_channels:
            self.update_status_message("You are already subscribed to SPS 101.")
            return
        self.client.subscribe_to_channel("SPS 101")
        self.client.subscribed_channels.add("SPS 101")
        self.update_status_message("You are now subscribed to SPS 101.")

    def unsubscribe_from_sps101(self):
        if not self.client.running:
            self.update_status_message("You must be connected to the server to unsubscribe.")
            return
        if "SPS 101" not in self.client.subscribed_channels:
            self.update_status_message("You are not subscribed to SPS 101.")
            return
        self.client.unsubscribe_from_channel("SPS 101")
        self.client.subscribed_channels.discard("SPS 101")
        self.update_status_message("You are now unsubscribed from SPS 101.")

    def update_status_message(self, message):
        self.status_messages.config(state='normal')
        self.status_messages.insert(tk.END, message + "\n")
        self.status_messages.config(state='disabled')
        self.status_messages.see(tk.END)  # Auto-scroll to the end

    def message_callback(self, message):
        # Schedule the update on the main thread
        self.master.after(0, lambda: self.handle_message(message))

    def handle_message(self, message):
        if message == "Server closed the connection.":
            self.on_connection_lost()
            return

    def on_connection_lost(self):
        # Perform GUI updates here
        self.connect_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.DISABLED)
        self.disable_subscription_buttons()
        self.update_status_message("Disconnected from server.")

    def on_close(self):
        # Perform clean-up actions here

        # If you have a client disconnect method
        if self.client:
            self.client.disconnect_from_server()

        # Destroy the window after clean-up
        self.master.destroy()

    def update_status(self, message):
        self.status_messages.config(state='normal')
        self.status_messages.insert(tk.END, message + "\n")
        self.status_messages.config(state='disabled')
        self.status_messages.see(tk.END)

    def update_channel_message(self, channel, username, message):
        channel_to_textbox = {
            "IF 100": self.if100_messages,
            "SPS 101": self.sps101_messages,
        }

        if channel in channel_to_textbox:
            self.update_text_box(channel_to_textbox[channel], username, message)
        else:
            print(f"Received message for unknown channel: {channel}")

    def update_text_box(self, text_widget, username, message):
        # Format the message with the username
        formatted_message = f"{username}: {message}\n"
        text_widget.config(state='normal')
        text_widget.insert(tk.END, formatted_message)  # Insert the formatted message
        text_widget.config(state='disabled')
        text_widget.see(tk.END)  # Auto-scroll to the end


# Create and run the client GUI
root = tk.Tk()
gui = ClientGUI(root)
root.mainloop()
