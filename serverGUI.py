import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox


from server import DiSUcordServer


class ServerGUI:
    def __init__(self, master):
        self.master = master
        master.title("DiSUcord Server")
        master.geometry("600x700")

        control_frame = tk.Frame(master)
        control_frame.grid(row=0, column=0, sticky="ew")

        tk.Label(control_frame, text="Server Port:").grid(row=0, column=0)
        self.port_entry = tk.Entry(control_frame)
        self.port_entry.grid(row=0, column=1)
        self.port_entry.insert(0, "12345")

        self.start_button = tk.Button(control_frame, text="Start Server", command=self.start_server)
        self.start_button.grid(row=0, column=2)

        self.stop_button = tk.Button(control_frame, text="Stop Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=3)

        self.log = scrolledtext.ScrolledText(master, state='disabled')
        self.log.grid(row=1, column=0, sticky="nsew")

        # In ServerGUI __init__

         # Label and Text Box for Connected Users
        tk.Label(master, text="Connected Users").grid(row=2, column=0, sticky="w")
        self.connected_clients_box = scrolledtext.ScrolledText(master, height=6, state='disabled')
        self.connected_clients_box.grid(row=3, column=0, sticky="nsew")

        # Label and Text Box for IF100 Subscribers
        tk.Label(master, text="IF100 Subscribers").grid(row=4, column=0, sticky="w")
        self.if100_subscribers_box = scrolledtext.ScrolledText(master, height=6, state='disabled')
        self.if100_subscribers_box.grid(row=5, column=0, sticky="nsew")

        # Label and Text Box for SPS101 Subscribers
        tk.Label(master, text="SPS101 Subscribers").grid(row=6, column=0, sticky="w")
        self.sps101_subscribers_box = scrolledtext.ScrolledText(master, height=6, state='disabled')
        self.sps101_subscribers_box.grid(row=7, column=0, sticky="nsew")

        self.server = DiSUcordServer()
        self.server_thread = None

        master.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_server(self):
        try:
            port = int(self.port_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid port number!")
            return

        self.server = DiSUcordServer()  # Reinitialize the server
        self.server.set_port(port)
        self.server.set_log_callback(self.update_log)
        self.server.set_gui(self)
        self.server_thread = threading.Thread(target=self.server.start)
        self.server_thread.start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_server(self):
        # Call the server's stop method
        if self.server:
            self.server.stop()

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log("Server stopped.")

    def update_log(self, message):
        self.log.config(state='normal')
        self.log.insert(tk.END, message + "\n")
        self.log.config(state='disabled')

    def update_connected_clients(self, client_list):
        def update():
            self.connected_clients_box.config(state='normal')
            self.connected_clients_box.delete(1.0, tk.END)
            self.connected_clients_box.insert(tk.END, "\n".join(client_list))
            self.connected_clients_box.config(state='disabled')

        self.master.after(0, update)

    def update_if100_subscribers(self, subscriber_list):
        def update():
            self.if100_subscribers_box.config(state='normal')
            self.if100_subscribers_box.delete(1.0, tk.END)
            self.if100_subscribers_box.insert(tk.END, "\n".join(subscriber_list))
            self.if100_subscribers_box.config(state='disabled')

        self.master.after(0, update)

    def update_sps101_subscribers(self, subscriber_list):
        def update():
            self.sps101_subscribers_box.config(state='normal')
            self.sps101_subscribers_box.delete(1.0, tk.END)
            self.sps101_subscribers_box.insert(tk.END, "\n".join(subscriber_list))
            self.sps101_subscribers_box.config(state='disabled')

        self.master.after(0, update)

    def on_close(self):
        # Stop the server if it is running
        if self.server and self.server.is_running:
            self.stop_server()

        # Explicitly destroy the GUI window
        self.master.destroy()


root = tk.Tk()
gui = ServerGUI(root)
root.mainloop()
