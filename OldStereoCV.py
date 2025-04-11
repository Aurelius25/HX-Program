import customtkinter as ctk
from tkinter import StringVar, IntVar
import pyperclip  
import datetime

class stereoCV:
    def __init__(self, root):
        self.root = root
        self.root.title("Optometry Testing Interface")
        self.root.geometry("1050x750")
        
        # Set the theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        
        # Create the main frame with light teal color
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#AADDD0")
        self.main_frame.pack(fill="both", expand=True)
        
        # Create header frame
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="#D0D0D0", height=30)
        self.header_frame.pack(fill="x", padx=5, pady=(5, 0))

        # Add tabs to header
        tabs = ["History", "Binocular", "Stereo/CV", "Perceptual", "Prim Reflexes", "Pictures", "ToDo", "Post Op", "Ex", "Ex 2", "Anterior", "Posterior"]
        for i, tab in enumerate(tabs):
            if i == 0:  # History tab is selected
                ctk.CTkLabel(self.header_frame, text=tab, fg_color="#D0D0D0", text_color="black", width=80).pack(side="left", padx=2, pady=2)
            else:
                ctk.CTkLabel(self.header_frame, text=tab, fg_color="#D0D0D0", text_color="black", width=80).pack(side="left", padx=2, pady=2)
        
        # Create content
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="#AADDD0")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create left buttons column
        self.left_column = ctk.CTkFrame(self.content_frame, fg_color="#AADDD0")
        self.left_column.pack(side="left", fill="y", padx=5)
        
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
                command=lambda t=btn_text: self.print_to_status(t)
            )
            btn.pack(pady=5, fill="x")

        self.new_line_button = ctk.CTkButton(self.main_frame, text="New Line", fg_color="#E090E0", 
                                            text_color="black", width=100, height=30,
                                            command=self.new_line)
        self.new_line_button.place(x=380, y=500)

        # Add large TNO button
        ctk.CTkButton(
            self.content_frame,
            text="Large TNO",
            fg_color="#FF69B4",
            text_color="black",
            corner_radius=2,
            width=120,
            height=30,
            command=lambda: self.print_to_status("Large TNO")
        ).place(x=180, y=125)
        
        # Create radio button groups
        self.create_radio_group("Randot Forms", [("500", 1), ("250", 2), ("None", 3)], 170, 10)
        self.create_radio_group("Randot Circles", [("400", 1), ("200", 2), ("140", 3), ("100", 4), ("70", 5)], 170, 50)
        self.create_radio_group("Randot Animals", [("50", 1), ("40", 2), ("30", 3), ("None", 4)], 170, 80)
        self.create_radio_group("TNO", [("100%", 1), ("50%", 2), ("None", 3)], 320, 130)
        self.create_radio_group("Range", [("100%", 1), ("70%", 2), ("50%", 3), ("No", 4), ("1m", 5), ("2m", 6), ("3m", 7)], 170, 200)
        self.create_radio_group("Ishihara", [("NAD", 1), ("Errors", 2), ("Defective", 3)], 170, 250)
        
        ctk.CTkLabel(self.content_frame, text="Put on", fg_color="#AADDD0").place(x=450, y=225)
        self.create_radio_group("Put on", [("+0.5", 1), ("+0.75", 2), ("Rx", 3)], 450, 250)
        self.create_status_bar()
        self.create_datetime_display()
        self.create_action_buttons()
        self.status_text = ""
        self.status_history = [""]

    def create_radio_group(self, name, options, x, y):
        var = IntVar()
        setattr(self, f"{name.replace(' ', '_').lower()}_var", var)
        
        for i, (text, value) in enumerate(options):
            radio = ctk.CTkRadioButton(
                self.content_frame,
                text=text,
                variable=var,
                value=value,
                command=lambda t=text: self.print_to_status(t)
            )
            radio.place(x=x + i*70, y=y)
    
    def print_to_status(self, text):
        self.status_history.append(self.status_text)
        
        if text == "New Line":
            self.status_text += "\n"
            self.status_textbox.insert("end", "\n")
        else:
            separator = " " if self.status_text and not self.status_text.endswith(" ") and not self.status_text.endswith("\n") else ""
            self.status_text += separator + text
            self.status_textbox.insert("end", separator + text)
        self.status_textbox.see("end")
    
    def copy_to_clipboard(self):
        pyperclip.copy(self.status_textbox.get(1.0, "end-1c"))
    
    def clear_status(self):
        # Save current state before clearing
        self.status_history.append(self.status_text)
        self.status_text = ""
        self.status_textbox.delete(1.0, "end")
    
    def undo_last_action(self):
        if len(self.status_history) > 1:
            self.status_history.pop()  # Remove current state
            self.status_text = self.status_history[-1]  # Get previous state
            self.status_textbox.delete(1.0, "end")
            self.status_textbox.insert("end", self.status_text)
            self.status_textbox.see("end")
    
    # Create status bar with textbox (from Binocular.py)
    def create_status_bar(self):
        self.status_textbox = ctk.CTkTextbox(self.main_frame, height=100, fg_color="#FFFFFF")
        self.status_textbox.pack(fill="x", side="bottom", padx=5, pady=5)
    
    # Create datetime display (from Binocular.py)
    def create_datetime_display(self):
        self.date_label = ctk.CTkLabel(self.content_frame, text="", font=("Arial", 12))
        self.date_label.place(x=90, y=350)
        
        self.time_label = ctk.CTkLabel(self.content_frame, text="", font=("Arial", 12))
        self.time_label.place(x=90, y=370)
        
        self.update_datetime()

    def update_datetime(self):
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        self.date_label.configure(text=f"Date: {date_str}")
        self.time_label.configure(text=f"Time: {time_str}")
        self.root.after(1000, self.update_datetime)
    
    # Create buttons for Copy All, Undo, and Clear (from Binocular.py)
    def create_action_buttons(self):
        x_cord = 700
        
        # Undo button
        undo_button = ctk.CTkButton(
            self.content_frame,
            text="Undo",
            fg_color="#FF0000",
            text_color="white",
            width=80,
            height=25,
            corner_radius=2,
            command=self.undo_last_action
        )
        undo_button.place(x=x_cord, y=140)
        
        # Clear button
        clear_button = ctk.CTkButton(
            self.content_frame,
            text="Clear",
            fg_color="#8B0000",
            text_color="white",
            width=80,
            height=25,
            corner_radius=2,
            command=self.clear_status
        )
        clear_button.place(x=x_cord, y=100)
        
        copy_button = ctk.CTkButton(
            self.content_frame,
            text="Copy All",
            fg_color="#DAA520",
            text_color="black",
            width=120,
            height=40,
            corner_radius=2,
            command=self.copy_to_clipboard
        )
        copy_button.place(x=x_cord, y=200)

    def new_line(self):
        self.status_history.append(self.status_text) 
        self.status_text += "\n"
        self.status_textbox.insert("end", "\n")
        self.status_textbox.see("end")    

if __name__ == "__main__":
    root = ctk.CTk()
    app = stereoCV(root)
    root.mainloop()