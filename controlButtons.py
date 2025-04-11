import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import pyperclip

class controlButtons:
    def __init__(self):
        super().__init__()

        self.createNewLineButton()

    def createNewLineButton(self, parent, width, height):
            #i think i fuked it up, check later
        button = ctk.CTkButton(parent, text='New Line', fg_color="#E090E0",
                               text_color="black", width=width, height=height)
        return button
                

        