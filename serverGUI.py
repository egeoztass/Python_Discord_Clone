import threading
import tkinter as tk
from tkinter import scrolledtext

from server import DiSUcordServer


class ServerGUI:
    def __init__(self, master):
        self.master = master
        master.title("DiSUcord Server")
        master.geometry("600x400")

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

        self.server = DiSUcordServer()
        self.server_thread = None

    def start_server(self):
        port = int(self.port_entry.get())
        self.server.set_port(port)
        self.server.set_log_callback(self.update_log)
        self.server_thread = threading.Thread(target=self.server.start)
        self.server_thread.start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_server(self):
        if self.server_thread and self.server_thread.is_alive():
            self.server.stop()
            self.server_thread.join()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.update_log("Server stopped")

    def update_log(self, message):
        self.log.config(state='normal')
        self.log.insert(tk.END, message + "\n")
        self.log.config(state='disabled')

root = tk.Tk()
gui = ServerGUI(root)
root.mainloop()
