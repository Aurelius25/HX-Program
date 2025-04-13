import customtkinter as ctk
import tkinter as tk

class Perceptual(ctk.CTkFrame):
    def __init__(self, master, root_app=None):
        ctk.CTkFrame.__init__(self, master, fg_color="#c2e6c2")
        self.root_app = root_app

         # Initialize timer variables
        self.timer_ids = {}

        # \u2713 check mark
        # \u2717 cross mark
        
        self.create_main_content()
        self.create_control_buttons()
        # self.bind("<Configure>", self.on_window_resize)

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
            
    def create_main_content(self):
        content_frame = ctk.CTkFrame(self, fg_color="#c2e6c2", corner_radius=0)
        content_frame.pack(fill="both", expand=False, pady=5)
        
        # Left column
        left_frame = ctk.CTkFrame(content_frame, fg_color="#c2e6c2", corner_radius=0, width=280)
        left_frame.pack(side="left", fill="y", padx=(0, 10), expand=False)
        
        # DEM sections
        self.dem_entries = {}  # Store entries for reference
        dem_labels = ["DEM A", "DEM B", "DEM C", "Skip line", "Rpt line"]
        
        for label in dem_labels:
            frame = ctk.CTkFrame(left_frame, fg_color="#c2e6c2", corner_radius=0, height=30)
            frame.pack(fill="x", pady=2)
            
            # Modify the command for each button - removed status updates
            if label in ["DEM A", "DEM B", "DEM C"]:
                label_button = ctk.CTkButton(
                    frame, 
                    text=label, 
                    fg_color="#f0f0f0", 
                    text_color="black", 
                    hover_color="#e0e0e0", 
                    corner_radius=5, 
                    height=25, 
                    width=80,
                    command=lambda l=label: self.toggle_increment_timer(l)
                )
            elif label in ["Skip line", "Rpt line"]:
                label_button = ctk.CTkButton(
                    frame, 
                    text=label, 
                    fg_color="#f0f0f0", 
                    text_color="black", 
                    hover_color="#e0e0e0", 
                    corner_radius=5, 
                    height=25, 
                    width=80,
                    command=lambda l=label: self.increment_entry(l)
                )
            else:
                label_button = ctk.CTkButton(
                    frame, 
                    text=label, 
                    fg_color="#f0f0f0", 
                    text_color="black", 
                    hover_color="#e0e0e0", 
                    corner_radius=5, 
                    height=25, 
                    width=80
                )
                
            label_button.pack(side="left", padx=5)
            
            entry = ctk.CTkEntry(frame, width=50, height=25, border_width=1)
            entry.pack(side="left", padx=10)
            entry.insert(0, "0")
            
            # Store entries in dictionary for later access
            self.dem_entries[label] = entry
        
        # Radio buttons
        radio_frame = ctk.CTkFrame(left_frame, fg_color="#c2e6c2", corner_radius=0)
        radio_frame.pack(fill="x", pady=5)
        
        radio_label = ctk.CTkLabel(radio_frame, text="Put on")
        radio_label.pack(side="left", padx=5)
        
        radio_var = tk.StringVar(value="+0.50")
        radio1 = ctk.CTkRadioButton(radio_frame, text="+0.5", variable=radio_var, value="+0.5",
                                   command=lambda: self.update_status("+0.50 RX"))
        radio1.pack(side="left", padx=5)
        
        radio2 = ctk.CTkRadioButton(radio_frame, text="+0.75", variable=radio_var, value="+0.75",
                                   command=lambda: self.update_status("+0.75 RX"))
        radio2.pack(side="left", padx=5)
        
        radio3 = ctk.CTkRadioButton(radio_frame, text="+1.00", variable=radio_var, value="+1.00",
                                   command=lambda: self.update_status("+1.00 RX"))
        radio3.pack(side="left", padx=5)
        
        button_frame = ctk.CTkFrame(left_frame, fg_color="#c2e6c2", corner_radius=0)
        button_frame.pack(fill="x", pady=10)
        
        self.done_button = ctk.CTkButton(
            button_frame, 
            text="Done", 
            fg_color="#4CAF50",
            text_color="white", 
            width=100, 
            height=30,
            command=self.calculate_dem_results 
        )
        self.done_button.pack(fill="x", pady=5)
        
        # New Line button (matching style from Binocular.txt)
        self.new_line_button = ctk.CTkButton(
            button_frame, 
            text="New Line", 
            fg_color="#E090E0",
            text_color="black", 
            width=100, 
            height=30,
            command=self.new_line
        )
        self.new_line_button.pack(fill="x", pady=5)
        
        monitor_btn = ctk.CTkButton(button_frame, text="Monroe V3", fg_color="#6699ff", 
                                    hover_color="#4d88ff", corner_radius=5, height=30,
                                    command=lambda: self.update_status("Monroe V3"))
        monitor_btn.pack(fill="x", pady=5)
        
    # Create control buttons with fixed positioning (updated to match Binocular.txt)
    def create_control_buttons(self):
        self.button_frame = ctk.CTkFrame(self, fg_color="#c2e6c2", corner_radius=0)
        self.button_frame.place(x=550, y=50)
        
        # Create the buttons within the frame
        self.undo_button = ctk.CTkButton(
            self.button_frame, 
            text="Undo", 
            fg_color="#A52A2A", 
            text_color="white", 
            width=100, 
            height=40,
            command=self.undo_status
        )
        self.undo_button.pack(pady=5)
        
        self.clear_status_button = ctk.CTkButton(
            self.button_frame, 
            text="Clear Status", 
            fg_color="#FF4500", 
            text_color="white", 
            width=100, 
            height=30,
            command=self.clear_status
        )
        self.clear_status_button.pack(pady=5)
        
        self.copy_button = ctk.CTkButton(
            self.button_frame, 
            text="Copy All", 
            fg_color="#A0A000", 
            text_color="black", 
            width=110, 
            height=50,
            command=self.copy_status
        )
        self.copy_button.pack(pady=5)
    
    # New function to calculate and display DEM results
    def calculate_dem_results(self):
        """Calculate DEM results and display them in the status bar"""
        try:
            # Get values from entry fields
            dem_a = int(self.dem_entries["DEM A"].get())
            dem_b = int(self.dem_entries["DEM B"].get())
            dem_c = int(self.dem_entries["DEM C"].get())
            skip_lines = int(self.dem_entries["Skip line"].get())
            rpt_lines = int(self.dem_entries["Rpt line"].get())
            
            # Calculate the results
            dem_ab_total = dem_a + dem_b
            total = dem_c + (4 * skip_lines) - (4 * rpt_lines)
            
            # Format the results message
            results_message = (
                f"DEMA = {dem_a}, "
                f"DEMB = {dem_b}, "
                f"DEMA + DEMB = {dem_ab_total}, "
                f"DEMC = {dem_c}, "
                f"Skip lines: {skip_lines}, "
                f"Rpt lines: {rpt_lines}, "
                f"Total = {total}"
            )
            
            # Update the status with the results
            self.update_status(results_message)
            
        except ValueError:
            # Handle case where entries contain non-numeric values
            self.update_status("Error: All DEM values must be numbers")
    
    
    def toggle_increment_timer(self, label):
        if label in self.timer_ids and self.timer_ids[label]:
            # Stop the timer
            self.after_cancel(self.timer_ids[label])
            self.timer_ids[label] = None
        else:
            # Start the timer
            self.increment_entry_with_timer(label)
    
    def increment_entry_with_timer(self, label):
        entry = self.dem_entries[label]
        current_value = int(entry.get())
        
        entry.delete(0, 'end')
        entry.insert(0, str(current_value + 1))
        
        # Schedule next increment
        self.timer_ids[label] = self.after(1000, lambda: self.increment_entry_with_timer(label))
    
    def increment_entry(self, label):
        """Increment the entry value once when button is pressed"""
        # Get current value
        entry = self.dem_entries[label]
        current_value = int(entry.get())
        
        # Increment the value
        entry.delete(0, 'end')
        entry.insert(0, str(current_value + 1))
    


             