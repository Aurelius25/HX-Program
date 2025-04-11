import customtkinter as ctk
import tkinter as tk

class History(ctk.CTkFrame):
    def __init__(self, master, root_app=None):
        ctk.CTkFrame.__init__(self, master)
        self.root_app = root_app