import tkinter as tk
import customtkinter as ctk
import pyperclip

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class binocular(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("HX Program")
        self.geometry("1050x750")
        
        # self.main_frame = ctk.CTkFrame(self, fg_color="#FAC8D4")
        self.main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.pack_propagate(False)

        self.subframe1 = ctk.CTkFrame(self.main_frame, border_color="black", border_width=1, width=850)
        self.subframe2 = ctk.CTkFrame(self.main_frame, border_color="black", border_width=1, width=200)
        self.subframe3 = ctk.CTkFrame(self.main_frame, border_color="black", border_width=1, width=200)

        self.subframe1.pack(side="left", fill="both")
        self.subframe2.pack(side="left", fill="y")
        self.subframe3.pack(side="left", fill="y")

        self.subframe1.pack_propagate(False)
        self.subframe2.pack_propagate(False)
        self.subframe3.pack_propagate(False)
        
        self.status_text = ""
        self.status_history = []
        
        # self.create_status_bar()
        self.create_top_buttons()
        # self.create_side_options()
        # self.create_number_grid()
        # self.create_movement_options()
        # self.create_plus_minus_buttons()
        # self.create_fatigue_slowing_options()
        # self.create_right_side_buttons()
        # self.create_tested_thru()
        # self.create_direction_buttons()
        # self.create_blue_buttons()
        
        # self.new_line_button = ctk.CTkButton(self.subframe1, text="New Line", fg_color="#E090E0", 
        #                                     text_color="black", width=100, height=30,
        #                                     command=self.new_line)
        # self.new_line_button.pack()
        
        # self.create_n_ret_dropdown()
        self.cm_toggle = False

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
        
    def toggle_cm(self):
        self.cm_toggle = not self.cm_toggle
        if self.cm_toggle:
            self.cm_radio.configure(text="cm (ON)")
        else:
            self.cm_radio.configure(text="cm (OFF)")

    def create_top_buttons(self):
        button_width = 85
        button_height = 30
        
        # Create frames to hold the buttons
        top_button_frame = ctk.CTkFrame(self.subframe1)
        top_button_frame.pack(pady=(80, 0))
        
        red_button_frame = ctk.CTkFrame(self.subframe1)
        red_button_frame.pack(pady=(10, 0))
        
        # First row buttons
        labels = ["DCT", "NCT", "NPC", "Pursuits", "N Ret"]
        colors = ["#FFA07A", "#FFA07A", "#FFA07A", "#FFA07A", "#FFA07A"]
        
        for i, label in enumerate(labels):
            if label != "N Ret":
                button = ctk.CTkButton(top_button_frame, text=label, fg_color=colors[i], 
                                    text_color="black", width=button_width, height=button_height,
                                    command=lambda l=label: self.update_status(l))
                button.pack(side="left", padx=7.5)
        
        # Second row buttons (red)
        red_labels = ["Near Phoria", "+2", "−2", "Dist Phoria"]
        red_commands = [
            lambda: self.update_status("Phoria @ 33cm"),
            lambda: self.update_status("Under +2:"),
            lambda: self.update_status("Under −2:"),
            lambda: self.update_status("Phoria @ 3m")
        ]
        
        for i, label in enumerate(red_labels):
            button = ctk.CTkButton(red_button_frame, text=label, fg_color="#FF6060", 
                                text_color="white", width=button_width, height=button_height,
                                command=red_commands[i])
            button.pack(side="left", padx=7.5)

    def create_n_ret_dropdown(self):
        n_ret_button = ctk.CTkButton(self.main_frame, text="N Ret", fg_color="#FFA07A", 
                                    text_color="black", width=85, height=30,
                                    command=self.show_n_ret_dropdown)
        n_ret_button.place(x=480, y=80)
        
        self.n_ret_dropdown = ctk.CTkFrame(self.main_frame, fg_color="#FFF0F0")
        self.n_ret_dropdown.place(x=480, y=110)
        self.n_ret_dropdown.place_forget()
        
        options = ["R", "L", "R&L", "Plano", "+0.25", "+0.50", "+0.75", "+1.00", "+1.25", "+1.50", "Close"]
        
        for i, option in enumerate(options):
            if option == "Close":
                button = ctk.CTkButton(self.n_ret_dropdown, text=option, 
                                      fg_color="#FF6060", text_color="white",
                                      width=100, height=25,
                                      command=self.close_n_ret_dropdown)
            else:
                button = ctk.CTkButton(self.n_ret_dropdown, text=option, 
                                      fg_color="#FFC0C0", text_color="black",
                                      width=100, height=25,
                                      command=lambda o=option: self.select_n_ret_option(o))
            button.grid(row=i, column=0, padx=5, pady=2)

    def show_n_ret_dropdown(self):
        self.update_status("Near Ret")
        self.n_ret_dropdown.place(x=480, y=110)

    def close_n_ret_dropdown(self):
        self.n_ret_dropdown.place_forget()

    def select_n_ret_option(self, option):
        self.update_status(option)

    def create_side_options(self):
        options = [("R", 530, 120), ("L", 530, 150), 
                ("P", 600, 120), ("T", 600, 150)]
        
        var1 = tk.StringVar(value="R")
        var2 = tk.StringVar(value="P")
        
        for opt, x, y in options:
            radio = ctk.CTkRadioButton(self.main_frame, text=opt, 
                                    variable=var1 if opt in ["R", "L"] else var2,
                                    value=opt,
                                    command=lambda o=opt: self.update_status(o))
            radio.place(x=x, y=y)
    
    # Create cm radio with background matching the main frame color (unlit state)
    # chagne to match the off colour
            self.cm_radio = ctk.CTkRadioButton(self.main_frame, text="cm (OFF)",
                                       variable=tk.StringVar(value="OFF"),
                                       value="ON",
                                       fg_color=self.main_frame._fg_color,  
                                       command=self.toggle_cm)
            self.cm_radio.place(x=670, y=120)

    def create_number_grid(self):
        ortho_button = ctk.CTkButton(self.main_frame, text="Ortho", fg_color="#FFFF60", 
                                    text_color="black", width=70, height=70,
                                    command=lambda: self.update_status("Ortho"))
        ortho_button.place(x=80, y=230)
        
        even_numbers = ["2", "4", "6", "8", "10", "12", "14", "16", "18", "20"]
        x_pos = 160
        for num in even_numbers:
            button = ctk.CTkButton(self.main_frame, text=num, fg_color="#90EE90", 
                                  text_color="black", width=30, height=30,
                                  command=lambda n=num: self.update_status(f"{n} {'cm' if self.cm_toggle else 'exo'}"))
            button.place(x=x_pos, y=230)
            x_pos += 35
        
        odd_numbers = ["1", "3", "5", "7", "9", "11", "13", "15", "17", "19", "21"]
        x_pos = 160
        for num in odd_numbers:
            button = ctk.CTkButton(self.main_frame, text=num, fg_color="#FFFF80", 
                                  text_color="black", width=30, height=30,
                                  command=lambda n=num: self.update_status(f"{n} {'cm' if self.cm_toggle else 'eso'}"))
            button.place(x=x_pos, y=270)
            x_pos += 35

    def create_movement_options(self):
        movement_options = ["Smooth", "Sl Jerky", "Jerky", "Conc poor", "Head Movt", "FROM"]
        var_movement = tk.StringVar(value="Smooth")
        
        for i, opt in enumerate(movement_options):
            if i == 0:
                x_pos = 95
            elif i == 1:
                x_pos = 180
            elif i == 2:
                x_pos = 270
            elif i == 3:
                x_pos = 340
            elif i == 4:
                x_pos = 450
            else:
                x_pos = 550
                
            radio = ctk.CTkRadioButton(self.main_frame, text=opt, variable=var_movement, value=opt,
                                      command=lambda o=opt: self.update_status(o))
            radio.place(x=x_pos, y=320)

    def create_plus_minus_buttons(self):
        buttons = [("\u00B1 2", 80, 360), ("\u00B1 1.5", 150, 360), 
                   ("\u00B1 1", 80, 400), ("\u00B1 0.5", 150, 400)]
        
        for text, x, y in buttons:
            num = text.split(" ")[1]
            button = ctk.CTkButton(self.main_frame, text=text, fg_color="#FFFF60", 
                                  text_color="black", width=60, height=30,
                                  command=lambda t=text, n=num: self.update_status(f"{t} facility"))
            button.place(x=x, y=y)
        
        bibo_button = ctk.CTkButton(self.main_frame, text="BI/BO", fg_color="#FFFF60", 
                                  text_color="black", width=60, height=30,
                                  command=lambda: self.update_status("8BI/12BO facility"))
        bibo_button.place(x=80, y=440)

    def create_fatigue_slowing_options(self):
        height1 = 350
        height2 = 380
        height3 = 410
        height4 = 440
        height5 = 470

        self.fatigue_slowing_var = tk.StringVar(value="+")
        
        grid_options = [
            ("\u2713 \u2713", 240, height1),
            ("\u2713", 240, height2),
            ("rapid", 240, height3),
            ("slow", 240, height4),
            ("just", 240, height5),
            
            ("Fail +", 320, height1),
            ("Fail -", 320, height2),
            ("Fail Both", 320, height3),
            ("Fail BO", 320, height4),
            ("Fail BI", 320, height5),
            
            ("Fatig +", 420, height1),
            ("Fatig -", 420, height2),
            ("Fatig Both", 420, height3),
            ("Fatig BO", 420, height4),
            ("Fatig BI", 420, height5),
            
            ("Slowing +", 520, height1),
            ("Slowing -", 520, height2),
            ("Slowing Both", 520, height3),
            ("Slowing BO", 520, height4),
            ("Slowing BI", 520, height5)
        ]
        
        for opt, x, y in grid_options:
            radio = ctk.CTkRadioButton(
                self.main_frame, 
                text=opt, 
                variable=self.fatigue_slowing_var,
                value=opt,
                command=lambda o=opt: self.update_status(o)
            )
            radio.place(x=x, y=y)

    def create_right_side_buttons(self):
        x_cord = 830

        undo_button = ctk.CTkButton(self.main_frame, text="Undo", fg_color="#A52A2A", 
                                  text_color="white", width=100, height=40,
                                  command=self.undo_status)
        undo_button.place(x=x_cord, y=130)
        
        clear_status_button = ctk.CTkButton(self.main_frame, text="Clear Status", fg_color="#FF4500", 
                                          text_color="white", width=100, height=30,
                                          command=self.clear_status)
        clear_status_button.place(x=x_cord, y=180)
        
        copy_button = ctk.CTkButton(self.main_frame, text="Copy All", fg_color="#A0A000", 
                                   text_color="black", width=110, height=50,
                                   command=self.copy_all)
        copy_button.place(x=x_cord, y=260)

    def create_blue_buttons(self):
        x_cord = 590
        y_cord = 230
        spacing = 40

        button3 = ctk.CTkButton(self.main_frame, text="Blur", fg_color="#4169E1", 
                               text_color="white", width=100, height=30,
                               command=lambda: self.update_status("Blur"))
        button3.place(x=x_cord, y=y_cord)
        
        button4 = ctk.CTkButton(self.main_frame, text="Suppress", fg_color="#4169E1", 
                               text_color="white", width=100, height=30,
                               command=lambda: self.update_status("Suppress"))
        button4.place(x=x_cord, y=y_cord+spacing)

    def create_tested_thru(self):
        tested_label = ctk.CTkLabel(self.main_frame, text="Tested thru")
        tested_label.place(x=780, y=380)
        
        options = [("Rx On", 780, 410), ("Plano", 780, 440)]
        var = tk.StringVar(value="Rx On")
        
        for opt, x, y in options:
            radio = ctk.CTkRadioButton(self.main_frame, text=opt, variable=var, value=opt,
                                      command=lambda o=opt: self.update_status(o))
            radio.place(x=x, y=y)
        
        bif_label = ctk.CTkLabel(self.main_frame, text="Tested Thru (BIF)")
        bif_label.place(x=80, y=480)
        
        options = [("T", 100, 510), ("B", 150, 510), ("T/B", 200, 510)]
        var_bif = tk.StringVar(value="T/B")
        
        # note: change to more aesthetic blue
        for opt, x, y in options:
            radio = ctk.CTkRadioButton(self.main_frame, text=opt, variable=var_bif, value=opt,
                                      command=lambda o=opt: self.update_status(o))
            radio.place(x=x, y=y)

    def create_direction_buttons(self):
        directions = [
            ("RH", 900, 380), 
            ("LH", 940, 380), 
            ("RE", 900, 420), 
            ("LE", 940, 420)
        ]
        
        for text, x, y in directions:
            button = ctk.CTkButton(self.main_frame, text=text, fg_color="#4169E1", 
                                  text_color="white", width=35, height=30,
                                  command=lambda t=text: self.update_status(t))
            button.place(x=x, y=y)

    def create_status_bar(self):
        self.status_textbox = ctk.CTkTextbox(self, height=100, fg_color="#FFFFFF")
        self.status_textbox.pack(fill="x", side="bottom", padx=5, pady=5)
        # No need to disable the textbox anymore

if __name__ == "__main__":
    app = binocular()
    app.mainloop()