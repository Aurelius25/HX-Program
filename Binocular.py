import customtkinter as ctk
import tkinter as tk

from ControlButtons import ControlButtons as ControlButtons

# note: fix action buttons and new line buttons

class Binocular(ctk.CTkFrame):
    def __init__(self, master, root_app=None):
        ctk.CTkFrame.__init__(self, master, fg_color="#FAC8D4")
        self.root_app = root_app
        self.cm_toggle = False
        self.button_spacing_x, self.button_spacing_y = 100, 40
        self.starting_pos_x = 40
        self.starting_pos_y = 40
        
        self.create_widgets()
        
    def create_widgets(self):
        self.create_top_buttons()
        self.create_n_ret_dropdown()
        self.create_side_options()
        self.create_number_grid()
        self.create_movement_options()
        self.create_plus_minus_buttons()
        self.create_fatigue_slowing_options()
        self.create_tested_thru()
        self.create_direction_buttons()
        self.create_blue_buttons()
        self.create_new_line_button()

        ControlButtons.create_action_buttons(self, self.starting_pos_x + 790,
                                             self.starting_pos_y + 120)
    
    def update_status(self, text):
        if self.root_app: self.root_app.main_update_status(text)
    
    def new_line(self):
        if self.root_app: self.root_app.main_new_line()
    
    def clear_status(self):
        if self.root_app: self.root_app.main_clear_status()
    
    def undo_status(self):
        if self.root_app: self.root_app.main_undo_status()
    
    def copy_status(self):
        if self.root_app: self.root_app.main_copy_status()

    def create_top_buttons(self):
        # Top row buttons
        labels = ["DCT", "NCT", "NPC", "Pursuits", "N Ret"]
        x_pos = self.starting_pos_x
        for i, label in enumerate(labels):
            if label != "N Ret":
                ctk.CTkButton(self, text=label, fg_color="#FFA07A", text_color="black", 
                              width=85, height=30, command=lambda l=label: self.update_status(l)).place(
                              x=x_pos, y=self.starting_pos_y)
                x_pos += self.button_spacing_x

        self.nret_button_x = self.starting_pos_x + 670
        self.nret_button_y = self.starting_pos_y

        self.n_ret_button = ctk.CTkButton(self, text="N Ret", fg_color="#FFA07A", text_color="black", 
                                         width=85, height=30, command=self.show_n_ret_dropdown)
        self.n_ret_button.place(x=self.nret_button_x, y=self.nret_button_y)
        
        # Second row red buttons
        red_labels = ["Near Phoria", "+2", "−2", "Dist Phoria"]
        red_commands = [
            lambda: self.update_status("Phoria @ 33cm"),
            lambda: self.update_status("Under +2:"),
            lambda: self.update_status("Under −2:"),
            lambda: self.update_status("Phoria @ 3m")
        ]
        
        x_pos = self.starting_pos_x
        for i, label in enumerate(red_labels):
            ctk.CTkButton(self, text=label, fg_color="#FF6060", text_color="white", 
                         width=85, height=30, command=red_commands[i]).place(
                         x=x_pos, y=self.starting_pos_y+self.button_spacing_y)
            x_pos += self.button_spacing_x

    def create_n_ret_dropdown(self):
        self.n_ret_dropdown = ctk.CTkFrame(self, fg_color="#FFF0F0")
        self.n_ret_dropdown.place(x=0, y=0)
        self.n_ret_dropdown.place_forget()
        self.n_ret_dropdown.lift()
        
        options = ["R", "L", "R&L", "Plano", "+0.25", "+0.50", "+0.75", "+1.00", "+1.25", "+1.50", "Close"]
        
        for i, option in enumerate(options):
            if option == "Close":
                cmd = self.close_n_ret_dropdown
                fg = "#FF6060"
                txt_color = "white"
            else:
                cmd = lambda o=option: self.select_n_ret_option(o)
                fg = "#FFC0C0"
                txt_color = "black"
                
            ctk.CTkButton(self.n_ret_dropdown, text=option, fg_color=fg, text_color=txt_color,
                         width=100, height=25, command=cmd).grid(row=i, column=0, padx=5, pady=2)

    def show_n_ret_dropdown(self):
        self.update_status("Near Ret")
        dropdown_y = self.nret_button_y + self.n_ret_button.winfo_height() + 5
        self.n_ret_dropdown.place(x=self.nret_button_x, y=dropdown_y)
        self.n_ret_dropdown.lift()

    def close_n_ret_dropdown(self):
        self.n_ret_dropdown.place_forget()

    def select_n_ret_option(self, option):
        self.update_status(option)

    def create_side_options(self):
        start_x = 530
        start_y = self.starting_pos_y + 90
        
        x_spacing = 70
        y_spacing = 30
        
        var1, var2 = tk.StringVar(value="R"), tk.StringVar(value="P")
        
        options = [
            ("R", 0, 0, var1), 
            ("L", 0, 1, var1), 
            ("P", 1, 0, var2), 
            ("T", 1, 1, var2)
        ]
        
        for opt, col, row, var in options:
            x = start_x + (col * x_spacing)
            y = start_y + (row * y_spacing)
            ctk.CTkRadioButton(self, text=opt, variable=var,
                            value=opt, command=lambda o=opt: self.update_status(o)).place(x=x, y=y)
    
        cm_y = start_y + (2 * y_spacing)
        self.cm_radio = ctk.CTkRadioButton(self, text="cm (OFF)", variable=tk.StringVar(value="OFF"),
                                        value="ON", command=self.toggle_cm)
        self.cm_radio.place(x=start_x, y=cm_y)

    def toggle_cm(self):
        self.cm_toggle = not self.cm_toggle
        self.cm_radio.configure(
            text=f"cm ({'ON' if self.cm_toggle else 'OFF'})",
            fg_color="#4f6be8" if self.cm_toggle else "#808080"
        )

    def create_number_grid(self):
        widget_spacing_y = 100
        
        # Ortho button
        ctk.CTkButton(self, text="Ortho", fg_color="#FFFF60", text_color="black", 
                     width=70, height=70, command=lambda: self.update_status("Ortho")).place(
                     x=self.starting_pos_x, y=self.starting_pos_y+widget_spacing_y)
        
        # Exo (even) numbers
        x_pos = self.starting_pos_x + 80
        for num in ["2", "4", "6", "8", "10", "12", "14", "16", "18", "20"]:
            ctk.CTkButton(self, text=num, fg_color="#90EE90", text_color="black", width=30, height=30,
                         command=lambda n=num: self.update_status(f"{n} {'cm' if self.cm_toggle else 'exo'}")).place(
                         x=x_pos, y=self.starting_pos_y+widget_spacing_y)
            x_pos += 35
        
        # Eso (odd) numbers
        x_pos = self.starting_pos_x + 80
        for num in ["1", "3", "5", "7", "9", "11", "13", "15", "17", "19", "21"]:
            ctk.CTkButton(self, text=num, fg_color="#FFFF80", text_color="black", width=30, height=30,
                         command=lambda n=num: self.update_status(f"{n} {'cm' if self.cm_toggle else 'eso'}")).place(
                         x=x_pos, y=self.starting_pos_y+widget_spacing_y+40)
            x_pos += 35

    def create_movement_options(self):
        movement_options = ["Smooth", "Sl Jerky", "Jerky", "Conc poor", "Head Movt", "FROM"]
        button_width = 80
        var_movement = tk.StringVar(value="Smooth")
        
        x_pos = self.starting_pos_x
        
        for opt in movement_options:
            ctk.CTkRadioButton(self, text=opt, variable=var_movement, value=opt,
                            command=lambda o=opt: self.update_status(o)).place(x=x_pos, y=self.starting_pos_y+200)
            # Adjust spacing based on text length
            spacing = max(len(opt) * 5 + 60, button_width)
            x_pos += spacing

    def create_plus_minus_buttons(self):
        start_x = self.starting_pos_x
        start_y = self.starting_pos_y + 250
        
        x_spacing = 70
        y_spacing = 40
        
        buttons = [("\u00B1 2", 0, 0), ("\u00B1 1.5", 1, 0), 
                ("\u00B1 1", 0, 1), ("\u00B1 0.5", 1, 1)]
        
        for text, col, row in buttons:
            num = text.split(" ")[1]
            x = start_x + (col * x_spacing)
            y = start_y + (row * y_spacing)
            ctk.CTkButton(self, text=text, fg_color="#FFFF60", text_color="black", width=60, height=30,
                        command=lambda t=text, n=num: self.update_status(f"{t} facility")).place(x=x, y=y)
        
        bi_bo_y = start_y + (2 * y_spacing)
        ctk.CTkButton(self, text="BI/BO", fg_color="#FFFF60", text_color="black", width=60, height=30,
                    command=lambda: self.update_status("8BI/12BO facility")).place(x=start_x, y=bi_bo_y)

    def create_fatigue_slowing_options(self):
        start_x = self.starting_pos_x + 160
        start_y = self.starting_pos_y + 250
        
        x_spacing = 100
        y_spacing = 30
        
        self.fatigue_slowing_var = tk.StringVar(value="+")
        
        options_grid = [
            [("\u2713 \u2713", 0), ("\u2713", 0), ("rapid", 0), ("slow", 0), ("just", 0)],
            [("Fail +", 1), ("Fail -", 1), ("Fail Both", 1), ("Fail BO", 1), ("Fail BI", 1)],
            [("Fatig +", 2), ("Fatig -", 2), ("Fatig Both", 2), ("Fatig BO", 2), ("Fatig BI", 2)],
            [("Slowing +", 3), ("Slowing -", 3), ("Slowing Both", 3), ("Slowing BO", 3), ("Slowing BI", 3)]
        ]
        
        for col_idx, col in enumerate(options_grid):
            for row_idx, (opt, col_offset) in enumerate(col):
                x = start_x + (col_offset * x_spacing)
                y = start_y + (row_idx * y_spacing)
                ctk.CTkRadioButton(self, text=opt, variable=self.fatigue_slowing_var, value=opt,
                                command=lambda o=opt: self.update_status(o)).place(x=x, y=y)

    def create_blue_buttons(self):
        start_x = 530
        start_y = self.starting_pos_y
        
        y_spacing = 40
        
        buttons = [("Blur", 0), ("Suppress", 1)]
        
        for text, row in buttons:
            y = start_y + (row * y_spacing)
            ctk.CTkButton(self, text=text, fg_color="#4169E1", text_color="white", 
                        width=100, height=30, command=lambda t=text: self.update_status(t)).place(x=start_x, y=y)

    def create_tested_thru(self):
        # Define position for regular tested through section
        regular_start_x = self.starting_pos_x + 580
        regular_start_y = self.starting_pos_y + 250
        
        # Define position for BIF tested through section
        bif_start_x = self.starting_pos_x
        bif_start_y = self.starting_pos_y + 380
        
        y_spacing = 30
        x_spacing = 50
        
        # Regular tested through
        ctk.CTkLabel(self, text="Tested thru").place(x=regular_start_x, y=regular_start_y)
        
        regular_options = [("rx On", 0), ("Plano", 1)]
        var = tk.StringVar(value="Rx On")
        
        for opt, row in regular_options:
            y = regular_start_y + ((row + 1) * y_spacing)  # +1 to account for the label
            ctk.CTkRadioButton(self, text=opt, variable=var, value=opt,
                            command=lambda o=opt: self.update_status(o)).place(x=regular_start_x, y=y)
        
        # BIF tested through
        ctk.CTkLabel(self, text="Tested Thru (BIF)").place(x=bif_start_x, y=bif_start_y)
        
        bif_options = [("T", 0), ("B", 1), ("T/B", 2)]
        var_bif = tk.StringVar(value="T/B")
        
        for opt, col in bif_options:
            x = bif_start_x + (col * x_spacing)  
            y = bif_start_y + y_spacing 
            ctk.CTkRadioButton(self, text=opt, variable=var_bif, value=opt,
                            command=lambda o=opt: self.update_status(o)).place(x=x, y=y)

    def create_direction_buttons(self):
        start_x = self.starting_pos_x + 790
        start_y = self.starting_pos_y + 300
        
        x_spacing = 55
        y_spacing = 40
        
        directions = [
            ("RH", 0, 0), 
            ("LH", 1, 0), 
            ("RE", 0, 1), 
            ("LE", 1, 1)
        ]
        
        for text, col, row in directions:
            x = start_x + (col * x_spacing)
            y = start_y + (row * y_spacing)
            ctk.CTkButton(self, text=text, fg_color="#4169E1", text_color="white", width=45, height=30,
                        command=lambda t=text: self.update_status(t)).place(x=x, y=y)

    def create_new_line_button(self):
        ctk.CTkButton(self, text="New Line", fg_color="#E090E0", text_color="black", 
                     width=100, height=30, command=self.new_line).place(x=self.starting_pos_x + 300, y=self.starting_pos_y + 400)