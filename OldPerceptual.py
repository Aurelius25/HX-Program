import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import pyperclip
import datetime

# Set appearance mode and default color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class Perceptual(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # TAAS
        # Make scrolable list with tick box
        # (cow)boy
        # steam(boat)
        # sun(shine) #1
        # (pic)nic
        # (cu)cumber
        # (c)oat
        # (m)eat
        # (t)ake
        # (ga)me
        # (wro)te
        # plea(se)
        # (c)lap
        # (p)lay
        # s(t)ale
        # s(m)ack #13

        # Configure window
        self.title("Medical Assessment Interface")
        self.geometry("1050x750")  # Reduced width since we're removing columns
        
        # Set background color to light green
        self.configure(fg_color="#c2e6c2")
        
        # Create the status bar frame at the bottom
        self.status_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", height=100)
        self.status_frame.pack(side="bottom", fill="x", padx=5, pady=5)
        self.status_frame.pack_propagate(False)  # Prevent the frame from resizing to fit contents
        
        # Create status textbox inside the status frame
        self.status_textbox = ctk.CTkTextbox(self.status_frame, fg_color="#FFFFFF")
        self.status_textbox.pack(fill="both", expand=True)
        
        # Initialize status variables
        self.status_text = ""
        self.status_history = []  # Changed to match Binocular.txt implementation
        
        # Create the main frame
        self.main_frame = ctk.CTkFrame(self, fg_color="#c2e6c2", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initialize timer variables
        self.timer_ids = {}
        
        self.create_header()
        self.create_tab_bar()
        self.create_main_content()
        self.create_control_buttons()
        # self.bind("<Configure>", self.on_window_resize)
        
    def create_header(self):
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="#c2e6c2", corner_radius=0, height=40)
        header_frame.pack(fill="x", pady=(0, 5))
        
        # Date and time display using datetime
        self.date_time_label = ctk.CTkLabel(header_frame, text="", font=("Arial", 14))
        self.date_time_label.pack(side="left", padx=10)
        self.update_datetime()
        
    def update_datetime(self):
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        self.date_time_label.configure(text=f"{date_str} {time_str}")
        
        # Update every second
        self.after(1000, self.update_datetime)
        
    def create_tab_bar(self):
        tab_frame = ctk.CTkFrame(self.main_frame, fg_color="#e6e6e6", corner_radius=0, height=30)
        tab_frame.pack(fill="x")
        
        tabs = ["History", "Binocular", "Stereo/CV", "Perceptual", "Prim Reflexes", 
                "Pictures", "ToDo", "Post Op", "Ex", "Ex 2", "Anterior", "Posterior"]
        
        for tab in tabs:
            tab_button = ctk.CTkButton(tab_frame, text=tab, fg_color="#e6e6e6", 
                                      text_color="black", hover_color="#d1d1d1", 
                                      corner_radius=0, height=30, width=70)
            tab_button.pack(side="left", padx=1)
            
    def create_main_content(self):
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="#c2e6c2", corner_radius=0)
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
        
        radio_var = tk.StringVar(value="+0.5")
        radio1 = ctk.CTkRadioButton(radio_frame, text="+0.5", variable=radio_var, value="+0.5",
                                   command=lambda: self.update_status("+0.50 RX"))
        radio1.pack(side="left", padx=10)
        
        radio2 = ctk.CTkRadioButton(radio_frame, text="+0.75", variable=radio_var, value="+0.75",
                                   command=lambda: self.update_status("+0.75 RX"))
        radio2.pack(side="left", padx=10)
        
        radio3 = ctk.CTkRadioButton(radio_frame, text="+1.00", variable=radio_var, value="+1.00",
                                   command=lambda: self.update_status("+1.00 RX"))
        radio3.pack(side="left", padx=10)
        
        button_frame = ctk.CTkFrame(left_frame, fg_color="#c2e6c2", corner_radius=0)
        button_frame.pack(fill="x", pady=10)
        
        self.done_button = ctk.CTkButton(
            button_frame, 
            text="Done", 
            fg_color="#4CAF50",  # Green color
            text_color="white", 
            width=100, 
            height=30,
            command=self.calculate_dem_results  # Modified to use our new function
        )
        self.done_button.pack(fill="x", pady=5)
        
        # New Line button (matching style from Binocular.txt)
        self.new_line_button = ctk.CTkButton(
            button_frame, 
            text="New Line", 
            fg_color="#E090E0",  # Using the color from Binocular.txt
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
        # Create a container frame for the buttons that's fixed at the bottom right
        self.button_frame = ctk.CTkFrame(self, fg_color="#c2e6c2", corner_radius=0)
        self.button_frame.place(x=550, y=100)
        
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
            command=self.copy_all
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
    
    # New functions for timer-based incrementation - removed status updates
    def toggle_increment_timer(self, label):
        """Toggle the timer for automatically incrementing the counter"""
        # Check if timer is already running
        if label in self.timer_ids and self.timer_ids[label]:
            # Stop the timer
            self.after_cancel(self.timer_ids[label])
            self.timer_ids[label] = None
        else:
            # Start the timer
            self.increment_entry_with_timer(label)
    
    def increment_entry_with_timer(self, label):
        """Increment the entry value every second and schedule next increment"""
        # Get current value
        entry = self.dem_entries[label]
        current_value = int(entry.get())
        
        # Increment the value
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
    
    # Functions for handling status updates (updated to match Binocular.txt)
    def update_status(self, text):
        # Save current status to history for undo
        self.status_history.append(self.status_text)
        
        # Add a space before the new text if the current text is not empty and doesn't end with space
        separator = " " if self.status_text and not self.status_text.endswith(" ") else ""
        self.status_text += separator + text
        
        # Move cursor to the end before inserting
        self.status_textbox.see("end")
        self.status_textbox.insert("end", separator + text)

    def new_line(self):
        # Save current status to history for undo
        self.status_history.append(self.status_text)
        self.status_text += "\n"
        self.status_textbox.insert("end", "\n")
        self.status_textbox.see("end")

    def clear_status(self):
        # Save current status to history for undo
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
        # Updated to match Binocular.txt implementation
        pyperclip.copy(self.status_textbox.get(1.0, "end-1c"))

if __name__ == "__main__":
    app = Perceptual()
    # Position buttons on startup after the window is fully initialized
    app.update_idletasks()
    # app.on_window_resize()
    app.mainloop()