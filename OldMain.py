import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import pyperclip
import datetime
import os
import sys

# import actionButtons

class main(ctk.CTk):    
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    def __init__(self):
        ctk.CTk().__init__(self, root)
        
        self.root = root
        self.root.title("Optometry Testing Interface")
        self.root.geometry("1050x750")
        self.root.minsize(1050,750)
        
        # Set the theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")        

        self.time_frame = ctk.CTkFrame(self.root, fg_color="#FF0000", height=50)
        self.tabs_frame = ctk.CTkFrame(self.root, fg_color="#e6e6e6", height=60)
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#0000FF")
        self.status_frame = ctk.CTkFrame(self.root, fg_color="#FFFFFF", height=120)

        self.time_frame.pack(fill='x')
        self.tabs_frame.pack(fill='x')
        self.main_frame.pack(fill='both', expand = True)
        self.status_frame.pack(fill='x')

        self.create_tab_bar()
        self.create_header()
        self.create_status_bar()

    def create_tab_bar(self):
        tab_frame = ctk.CTkFrame(self.tabs_frame, fg_color="#e6e6e6", corner_radius=0, height=30)
        tab_frame.pack(fill="x")
        
        tabs = ["History", "Binocular", "Stereo/CV", "Perceptual", "Prim Reflexes", 
                "Pictures", "ToDo", "Post Op", "Ex", "Ex 2", "Anterior", "Posterior"]
        
        for tab in tabs:
            tab_button = ctk.CTkButton(tab_frame, text=tab, fg_color="#e6e6e6", 
                                      text_color="black", hover_color="#d1d1d1", 
                                      corner_radius=0, height=30, width=70)
            tab_button.pack(side="left", padx=1)

    def create_header(self):
        header_frame = ctk.CTkFrame(self.time_frame, fg_color="#00FFFF", corner_radius=0, height=40)
        header_frame.pack(fill="x", pady=(0, 0))
        self.date_time_label = ctk.CTkLabel(header_frame, text="", font=("Arial", 14))
        self.date_time_label.pack(side="left", padx=10)
        self.update_datetime()
        
    def create_status_bar(self):
       self.status_textbox = ctk.CTkTextbox(self.status_frame, height=100, fg_color="#FFFFFF")
       self.status_textbox.pack(fill="x", side="bottom", padx=5, pady=5)

    def update_datetime(self):
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        self.date_time_label.configure(text=f"{date_str} {time_str}")
        self.root.after(1000, self.update_datetime)

    def update_status(self, text):
        self.status_history.append(self.status_text)
        # Add a space before the new text if the current text is not empty
        separator = " " if self.status_text and not self.status_text.endswith(" ") else ""
        self.status_text += separator + text
        
        # Move cursor to the end before inserting
        self.status_textbox.see("end")
        self.status_textbox.insert("end", separator + text)

    def new_line(self):
        self.status_history.append(self.status_text)
        self.status_text += "\n"
        self.status_textbox.insert("end", "\n")
        self.status_textbox.see("end")

    def clear_status(self):
        self.status_history.append(self.status_text)
        self.status_text = ""
        self.status_textbox.delete(1.0, "end")

    def undo_status(self):
        if self.status_history:
            self.status_text = self.status_history.pop()
            self.status_textbox.delete(1.0, "end")
            self.status_textbox.insert("end", self.status_text)
            self.status_textbox.see("end")       

    def copy_all(self):
        pyperclip.copy(self.status_textbox.get(1.0, "end-1c"))                  
       
if __name__ == "__main__":
    root = ctk.CTk()
    app = main()
    root.mainloop()