import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import pyperclip

class ControlButtons:
    def __init__(self):
        super().__init__()
        
        self.button_configs = [
            ("Undo", "#A52A2A", "white", 100, 40, 0),
            ("Clear Status", "#FF4500", "white", 100, 30, 50),
            ("Copy All", "#A0A000", "black", 100, 50, 100)
        ]
        
    @staticmethod
    def create_action_buttons(parent, x_cord, y_cord):
        # Create an instance to access the button configs
        control_buttons = ControlButtons()
        
        commands = [parent.undo_status, parent.clear_status, parent.copy_status]
        
        for i, (text, fg, txt_color, w, h, y_offset) in enumerate(control_buttons.button_configs):
            ctk.CTkButton(parent, 
                          text=text, 
                          fg_color=fg, 
                          text_color=txt_color, 
                          width=w, 
                          height=h, 
                          command=commands[i]).place(x=x_cord, y=y_cord + y_offset)

    def create_new_line_button(parent, width, height, x_cord, y_cord):
        pass