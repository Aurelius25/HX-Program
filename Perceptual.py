import customtkinter as ctk
import tkinter as tk

class Perceptual(ctk.CTkFrame):
    def __init__(self, master, root_app=None):
        ctk.CTkFrame.__init__(self, master, fg_color="#c2e6c2")
        self.root_app = root_app