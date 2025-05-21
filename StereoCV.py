import customtkinter as ctk
import tkinter as tk
from tkinter import StringVar, IntVar

from ControlButtons import ControlButtons as ControlButtons

class StereoCV(ctk.CTkFrame):
    def __init__(self, master, root_app=None):
        # colours
        self.background_colour = "#99fdff" # blue
        self.button_colour = "#FF69B4" # pink

        ctk.CTkFrame.__init__(self, master, fg_color=self.background_colour)
        self.root_app = root_app

        self.y_pos_randot_forms = 10  
        self.y_pos_randot_circles = 60  
        self.y_pos_randot_animals = 100  
        self.y_pos_tno = 160  
        self.y_pos_range = 220 
        self.y_pos_ishihara = 280

        # Create content
        self.content_frame = ctk.CTkFrame(self, fg_color=self.background_colour)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create left buttons column
        self.left_column = ctk.CTkFrame(self.content_frame, fg_color=self.background_colour)
        self.left_column.pack(side="left", fill="y", padx=5)

        self.create_pink_buttons()
        self.create_radio_group("Randot Forms", [("500", 1), ("250", 2), ("None", 3)], 170, self.y_pos_randot_forms + 3)
        self.create_radio_group("Randot Circles", [("400", 1), ("200", 2), ("140", 3), ("100", 4), ("70", 5)], 170, self.y_pos_randot_circles)
        self.create_radio_group("Randot Animals", [("50", 1), ("40", 2), ("30", 3), ("None", 4)], 170, self.y_pos_randot_animals)
        self.create_radio_group("TNO", [("100%", 1), ("50%", 2), ("None", 3)], 320, self.y_pos_tno)
        self.create_radio_group("Range", [("100%", 1), ("70%", 2), ("50%", 3), ("No", 4), ("1m", 5), ("2m", 6), ("3m", 7)], 170, self.y_pos_range)
        self.create_radio_group("Ishihara", [("NAD", 1), ("Errors", 2), ("Defective", 3)], 170, self.y_pos_ishihara)
        self.create_radio_group("Put on", [("+0.50", 1), ("+0.75", 2), ("rx", 3)], 450, self.y_pos_ishihara)

        # Put on label - position relative to ishihara variable
        ctk.CTkLabel(self.content_frame, text="Put on", fg_color=self.background_colour).place(x=450, y=self.y_pos_ishihara - 30)

        ControlButtons.create_action_buttons(self, 830, 160)

    def update_status(self, text):
        if self.root_app:
            self.root_app.main_update_status(text)  

    def new_line(self):
        if self.root_app:
            self.root_app.main_new_line()  

    def clear_status(self):
        if self.root_app:
            self.root_app.main_clear_status()  

    def undo_status(self):
        if self.root_app:
            self.root_app.main_undo_status()

    def copy_status(self):
        if self.root_app:
            self.root_app.main_copy_status()    

    def create_pink_buttons(self):
        # Create pink buttons dictionary with positions - using the instance variables
        pink_buttons = [
            {"text": "Randot Forms", "y_pos": self.y_pos_randot_forms},
            {"text": "Randot Circles", "y_pos": self.y_pos_randot_circles},
            {"text": "Randot Animals", "y_pos": self.y_pos_randot_animals},
            {"text": "TNO", "y_pos": self.y_pos_tno},
            {"text": "Large Range", "y_pos": self.y_pos_range},
            {"text": "Ishihara", "y_pos": self.y_pos_ishihara}
        ]
        
        # Create buttons based on the dictionary using place() instead of pack()
        button_width = 120  # Width for all buttons
        button_height = 30  # Height for all buttons
        button_x = 10       # X position for all buttons in left column
        
        for btn_data in pink_buttons:
            btn = ctk.CTkButton(
                self.left_column,
                text=btn_data["text"],
                fg_color=self.button_colour,
                text_color="black",
                width=button_width,
                height=button_height,
                command=lambda t=btn_data["text"]: self.update_status(t)
            )
            btn.place(x=button_x, y=btn_data["y_pos"])

        # Add large TNO button - now using the TNO position variable
        ctk.CTkButton(
            self.content_frame,
            text="Large TNO",
            fg_color=self.button_colour,
            text_color="black",
            width=120,
            height=30,
            command=lambda: self.update_status("Large TNO")
        ).place(x=180, y=self.y_pos_tno - 5)  # Small offset to align nicely

    def create_radio_group(self, name, options, x, y):
        var = IntVar()
        setattr(self, f"{name.replace(' ', '_').lower()}_var", var)
        
        for i, (text, value) in enumerate(options):
            radio = ctk.CTkRadioButton(
                self.content_frame,
                text=text,
                variable=var,
                value=value,
                command=lambda t=text: self.update_status(t)
            )
            radio.place(x=x + i*70, y=y)