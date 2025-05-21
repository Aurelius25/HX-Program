import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import pyperclip
import datetime
import os
import sys

from Binocular import Binocular as Binocular
from Perceptual import Perceptual as Perceptual
from StereoCV import StereoCV as StereoCV

# Operating Notes:
# Perceptual: undo does not work when doing the test, just use the clear status button

# main improvements
# in the binocular class fix the cm toggle 

# code improvementes
# in each class make colours, properites of each class

# completed
# on sterero CV lined up Ishihara button with NAD
# on perceptual print the result to status bar
# on perceptual make the text say w/ +0.50 rx
# make text print w/ +0.50 rx
# on perceptual print tvas, mvpt and taas
# on perceptual add feature that prints in set order


class Main(ctk.CTk):
    # @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    
    def __init__(self):
        ctk.CTk.__init__(self)    

        self.status_text = ""
        self.status_history = []

        self.time_frame = ctk.CTkFrame(self, height=50)
        self.tabs_frame = ctk.CTkFrame(self, fg_color="#e6e6e6", height=60)
        self.main_frame = ctk.CTkFrame(self)
        self.status_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", height=120)

        self.time_frame.pack(fill='x')
        self.tabs_frame.pack(fill='x')
        self.main_frame.pack(fill='both', expand=True)
        self.status_frame.pack(fill='x')

        # Initialize the frame placeholder
        self._frame = None
        self.switch_frame(BinocularTabContent)

        self.create_tab_bar()
        self.create_datetime_display()
        self.create_status_bar()

    def switch_frame(self, frame_class):
        # Create a new instance of the frame class
        new_frame = frame_class(self.main_frame, self)
        
        # Destroy previous frame if it exists
        if self._frame is not None:
            self._frame.destroy()
            
        # Set the new frame and display it
        self._frame = new_frame
        self._frame.pack(fill="both", expand=True)
    
    def create_datetime_display(self):    
        self.date_label = ctk.CTkLabel(self.time_frame, text="", font=("Arial", 15))
        self.time_label = ctk.CTkLabel(self.time_frame, text= "", font=("Arial", 15))
        self.date_label.pack(side="left", padx="20")
        self.time_label.pack(side="left", padx="10")
        self.update_datetime()

    def update_datetime(self):
        now = datetime.datetime.now()
        date_str = now.strftime("%Y/%m/%d")
        time_str = now.strftime("%H:%M:%S")
        self.date_label.configure(text=f"Date: {date_str}")
        self.time_label.configure(text=f"Time: {time_str}")
        self.after(1000, self.update_datetime)      

    def create_status_bar(self):
       self.status_textbox = ctk.CTkTextbox(self.status_frame, height=100, fg_color="#FFFFFF")
       self.status_textbox.pack(fill="x", side="bottom", padx=5, pady=5)

    def create_tab_bar(self):
        tab_frame = ctk.CTkFrame(self.tabs_frame, fg_color="#e6e6e6", corner_radius=0, height=30)
        tab_frame.pack(fill="x")
    
        # Define tab-to-class mapping
        tab_mapping = {
            "Binocular": BinocularTabContent,
            "Stereo/CV": StereoTabContent,
            "Perceptual": PerceptualTabContent,
        }

        # tabs = ["History", "Binocular", "Stereo/CV", "Perceptual", "Prim Reflexes", 
        #         "Pictures", "ToDo", "Post Op", "Ex", "Ex 2", "Anterior", "Posterior"]
        
        # Create tab buttons
        for tab_name, tab_class in tab_mapping.items():
            tab_button = ctk.CTkButton(tab_frame, text=tab_name, fg_color="#e6e6e6", 
                                       text_color="black", hover_color="#d1d1d1", 
                                       corner_radius=0, height=30, width=70,
                                       command=lambda cls=tab_class: self.switch_frame(cls))
            
            tab_button.pack(side="left", padx=1)

    # Method to update status bar
    def main_update_status(self, text):
        self.status_history.append(self.status_text)
        # Add a space before the new text if the current text is not empty
        separator = " " if self.status_text and not self.status_text.endswith(" ") else ""
        self.status_text += separator + text
        
        # Move cursor to the end before inserting
        self.status_textbox.see("end")
        self.status_textbox.insert("end", separator + text)

    def main_clear_status(self):
        self.status_history.append(self.status_text)
        self.status_text = ""
        self.status_textbox.delete(1.0, "end") 

    def main_undo_status(self):
        if self.status_history:
            self.status_text = self.status_history.pop()
            self.status_textbox.delete(1.0, "end")
            self.status_textbox.insert("end", self.status_text)
            self.status_textbox.see("end")

    def main_copy_status(self):
        pyperclip.copy(self.status_textbox.get(1.0, "end-1c"))

    def main_new_line(self):
        self.status_history.append(self.status_text)
        self.status_text += "\n"
        self.status_textbox.insert("end", "\n")
        self.status_textbox.see("end")

# Binocular Tab Content
class BinocularTabContent(Binocular):
    def __init__(self, master, root_app):
        Binocular.__init__(self, master, root_app)

# Stereo/CV Tab Content
class StereoTabContent(StereoCV):
    def __init__(self, master, root_app):
        StereoCV.__init__(self, master, root_app)

# Perceptual Tab Content
class PerceptualTabContent(Perceptual):
    def __init__(self, master, root_app):
        Perceptual.__init__(self, master, root_app)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Hope you don't find this bit cause I think I'll get smacked for this
    # but I made this cause I like you, 
    # I don't expect anything back
    # that also why I felt guilty about the league skin
    # please don't feel like you owe me anything

    app = Main()
    app.title("HX Program")
    app.geometry("1050x750")
    app.minsize(1050, 750)
    app.mainloop()