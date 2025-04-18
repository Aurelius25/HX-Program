import customtkinter as ctk
import tkinter as tk
from tkinter import StringVar, IntVar

# note: i want to redo this using pack instead of place
# not sure if i ilke using the fucntion to create the buttons, but will change later

class StereoCV(ctk.CTkFrame):
    def __init__(self, master, root_app=None):

        # colours
        # rename the colours to actual names
        self.background_colour = "#57dee6"

        ctk.CTkFrame.__init__(self, master, fg_color=self.background_colour)
        self.root_app = root_app


        # Create content
        self.content_frame = ctk.CTkFrame(self, fg_color=self.background_colour)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create left buttons column
        self.left_column = ctk.CTkFrame(self.content_frame, fg_color=self.background_colour)
        self.left_column.pack(side="left", fill="y", padx=5)

        self.create_pink_buttons()
        self.create_action_buttons()
        self.create_radio_group("Randot Forms", [("500", 1), ("250", 2), ("None", 3)], 170, 10)
        self.create_radio_group("Randot Circles", [("400", 1), ("200", 2), ("140", 3), ("100", 4), ("70", 5)], 170, 50)
        self.create_radio_group("Randot Animals", [("50", 1), ("40", 2), ("30", 3), ("None", 4)], 170, 80)
        self.create_radio_group("TNO", [("100%", 1), ("50%", 2), ("None", 3)], 320, 130)
        self.create_radio_group("Range", [("100%", 1), ("70%", 2), ("50%", 3), ("No", 4), ("1m", 5), ("2m", 6), ("3m", 7)], 170, 200)
        self.create_radio_group("Ishihara", [("NAD", 1), ("Errors", 2), ("Defective", 3)], 170, 250)
        self.create_radio_group("Put on", [("+0.50", 1), ("+0.75", 2), ("Rx", 3)], 450, 250)

        ctk.CTkLabel(self.content_frame, text="Put on", fg_color="#AADDD0").place(x=450, y=225)

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
        # Create pink buttons
        pink_buttons = ["Randot Forms", "Randot Circles", "Randot Animals", "TNO", "Large Range", "Ishihara"]
        for btn_text in pink_buttons:
            btn = ctk.CTkButton(
                self.left_column,
                text=btn_text,
                fg_color="#FF69B4",
                text_color="black",
                corner_radius=2,
                height=30,
                command=lambda t=btn_text: self.update_status(t)
            )
            btn.pack(pady=5, fill="x")

        # Add large TNO button
        ctk.CTkButton(
            self.content_frame,
            text="Large TNO",
            fg_color="#FF69B4",
            text_color="black",
            corner_radius=2,
            width=120,
            height=30,
            command=lambda: self.update_status("Large TNO")
        ).place(x=180, y=125)
    
    def create_action_buttons(self):
        x_cord = 830

        undo_button = ctk.CTkButton(self, text="Undo", fg_color="#A52A2A", 
                                  text_color="white", width=100, height=40,
                                  command=self.undo_status)
        undo_button.place(x=x_cord, y=130)
        
        clear_status_button = ctk.CTkButton(self, text="Clear Status", fg_color="#FF4500", 
                                          text_color="white", width=100, height=30,
                                          command=self.clear_status)
        clear_status_button.place(x=x_cord, y=180)
        
        copy_button = ctk.CTkButton(self, text="Copy All", fg_color="#A0A000", 
                                   text_color="black", width=110, height=50,
                                   command=self.copy_status)
        copy_button.place(x=x_cord, y=260)

        self.new_line_button = ctk.CTkButton(self, text="New Line", fg_color="#E090E0", 
                                            text_color="black", width=100, height=30,
                                            command=self.new_line)
        self.new_line_button.place(x=380, y=350)


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