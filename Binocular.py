import customtkinter as ctk
import tkinter as tk

# note: need to move around the widgets, but mostly works

class Binocular(ctk.CTkFrame):
    def __init__(self, master, root_app=None):
        ctk.CTkFrame.__init__(self, master, fg_color="#FAC8D4")
        self.root_app = root_app
        
        self.cm_toggle = False  

        self.create_top_buttons()
        self.create_n_ret_dropdown()
        self.create_side_options()
        self.create_number_grid()
        self.create_movement_options()
        self.create_plus_minus_buttons()
        self.create_fatigue_slowing_options()
        self.create_right_side_buttons()
        self.create_tested_thru()
        self.create_direction_buttons()
        self.create_blue_buttons()
        self.create_new_line_button()
        
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

    def create_top_buttons(self):
        button_width = 85
        button_spacing = 100
        
        labels = ["DCT", "NCT", "NPC", "Pursuits", "N Ret"]
        colors = ["#FFA07A", "#FFA07A", "#FFA07A", "#FFA07A", "#FFA07A"]
        
        x_pos = 80
        for i, label in enumerate(labels):
            if label != "N Ret":
                button = ctk.CTkButton(self, text=label, fg_color=colors[i], 
                                      text_color="black", width=button_width, height=30,
                                      command=lambda l=label: self.update_status(l))
                button.place(x=x_pos, y=80)
                x_pos += button_spacing
        
        red_labels = ["Near Phoria", "+2", "−2", "Dist Phoria"]
        red_commands = [
            lambda: self.update_status("Phoria @ 33cm"),
            lambda: self.update_status("Under +2:"),
            lambda: self.update_status("Under −2:"),
            lambda: self.update_status("Phoria @ 3m")
        ]
        
        x_pos = 80
        for i, label in enumerate(red_labels):
            button = ctk.CTkButton(self, text=label, fg_color="#FF6060", 
                                  text_color="white", width=button_width, height=30,
                                  command=red_commands[i])
            button.place(x=x_pos, y=120)
            x_pos += button_spacing        

    def create_n_ret_dropdown(self):
        n_ret_button = ctk.CTkButton(self, text="N Ret", fg_color="#FFA07A", 
                                    text_color="black", width=85, height=30,
                                    command=self.show_n_ret_dropdown)
        n_ret_button.place(x=480, y=80)
        
        self.n_ret_dropdown = ctk.CTkFrame(self, fg_color="#FFF0F0")
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
            radio = ctk.CTkRadioButton(self, text=opt, 
                                    variable=var1 if opt in ["R", "L"] else var2,
                                    value=opt,
                                    command=lambda o=opt: self.update_status(o))
            radio.place(x=x, y=y)
    
    # Create cm radio with background matching the main frame color (unlit state)
            self.cm_radio = ctk.CTkRadioButton(self, text="cm (OFF)",
                                       variable=tk.StringVar(value="OFF"),
                                       value="ON",
                                       command=self.toggle_cm)
            self.cm_radio.place(x=670, y=120)    

    # note: still need to fix radio button
    def toggle_cm(self):
        self.cm_toggle = not self.cm_toggle
        if self.cm_toggle:
            self.cm_radio.configure(text="cm (ON)", fg_color="#4f6be8")
        else:
            self.cm_radio.configure(text="cm (OFF)", fg_color="#808080")         

    def create_number_grid(self):
        ortho_button = ctk.CTkButton(self, text="Ortho", fg_color="#FFFF60", 
                                    text_color="black", width=70, height=70,
                                    command=lambda: self.update_status("Ortho"))
        ortho_button.place(x=80, y=230)
        
        even_numbers = ["2", "4", "6", "8", "10", "12", "14", "16", "18", "20"]
        x_pos = 160
        for num in even_numbers:
            button = ctk.CTkButton(self, text=num, fg_color="#90EE90", 
                                  text_color="black", width=30, height=30,
                                  command=lambda n=num: self.update_status(f"{n} {'cm' if self.cm_toggle else 'exo'}"))
            button.place(x=x_pos, y=230)
            x_pos += 35
        
        odd_numbers = ["1", "3", "5", "7", "9", "11", "13", "15", "17", "19", "21"]
        x_pos = 160
        for num in odd_numbers:
            button = ctk.CTkButton(self, text=num, fg_color="#FFFF80", 
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
                
            radio = ctk.CTkRadioButton(self, text=opt, variable=var_movement, value=opt,
                                      command=lambda o=opt: self.update_status(o))
            radio.place(x=x_pos, y=320)

    def create_plus_minus_buttons(self):
        buttons = [("\u00B1 2", 80, 360), ("\u00B1 1.5", 150, 360), 
                   ("\u00B1 1", 80, 400), ("\u00B1 0.5", 150, 400)]
        
        for text, x, y in buttons:
            num = text.split(" ")[1]
            button = ctk.CTkButton(self, text=text, fg_color="#FFFF60", 
                                  text_color="black", width=60, height=30,
                                  command=lambda t=text, n=num: self.update_status(f"{t} facility"))
            button.place(x=x, y=y)
        
        bibo_button = ctk.CTkButton(self, text="BI/BO", fg_color="#FFFF60", 
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
                self, 
                text=opt, 
                variable=self.fatigue_slowing_var,
                value=opt,
                command=lambda o=opt: self.update_status(o)
            )
            radio.place(x=x, y=y)

    def create_right_side_buttons(self):
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

    def create_blue_buttons(self):
        x_cord = 590
        y_cord = 230
        spacing = 40

        button3 = ctk.CTkButton(self, text="Blur", fg_color="#4169E1", 
                               text_color="white", width=100, height=30,
                               command=lambda: self.update_status("Blur"))
        button3.place(x=x_cord, y=y_cord)
        
        button4 = ctk.CTkButton(self, text="Suppress", fg_color="#4169E1", 
                               text_color="white", width=100, height=30,
                               command=lambda: self.update_status("Suppress"))
        button4.place(x=x_cord, y=y_cord+spacing)

    def create_tested_thru(self):
        tested_label = ctk.CTkLabel(self, text="Tested thru")
        tested_label.place(x=780, y=380)
        
        options = [("Rx On", 780, 410), ("Plano", 780, 440)]
        var = tk.StringVar(value="Rx On")
        
        for opt, x, y in options:
            radio = ctk.CTkRadioButton(self, text=opt, variable=var, value=opt,
                                      command=lambda o=opt: self.update_status(o))
            radio.place(x=x, y=y)
        
        bif_label = ctk.CTkLabel(self, text="Tested Thru (BIF)")
        bif_label.place(x=80, y=480)
        
        options = [("T", 100, 510), ("B", 150, 510), ("T/B", 200, 510)]
        var_bif = tk.StringVar(value="T/B")
        
        for opt, x, y in options:
            radio = ctk.CTkRadioButton(self, text=opt, variable=var_bif, value=opt,
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
            button = ctk.CTkButton(self, text=text, fg_color="#4169E1", 
                                  text_color="white", width=35, height=30,
                                  command=lambda t=text: self.update_status(t))
            button.place(x=x, y=y)    

    def create_new_line_button(self):
        self.new_line_button = ctk.CTkButton(self, text="New Line", fg_color="#E090E0", 
                                            text_color="black", width=100, height=30,
                                            command=self.new_line)
        self.new_line_button.place(x=380, y=500)  
             