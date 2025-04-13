
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import pyperclip
import datetime
from PIL import Image, ImageDraw
import os

# note: bug where it only will print TAAS, TVAS, MVPT once then have to full reset
# note: add function that resets all checkboxes on clear status, currently it doesn't bug too bad
# note: if you press the NG button and there is no number there it breaks, maybe add disable 
#       feature if i cant fix it
# note need to add feature which keeps the thingys in order, redundancy
# note: don't do multiple test at once, don't think i need to mention this tho
# note: current method is to check how many green boxes there are, alt. to check amount of ticks
# note: have to click the first button for it to print TVAS, TAAS, MVPT 

# note: might need to make it mode based

# Set appearance mode and default color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class Perceptual(ctk.CTk):
    def __init__(self):
        super().__init__()
        
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
        
        # Dictionary to track labels in status bar
        self.status_labels = {}
        
        # Track if first button in each section has been clicked
        self.first_taas_clicked = False
        self.first_tvas_clicked = False
        self.first_mvpt_clicked = False
        
        # Create the main frame
        self.main_frame = ctk.CTkFrame(self, fg_color="#c2e6c2", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initialize timer variables
        self.timer_ids = {}
        
        self.create_main_content()
        self.create_control_buttons()
        self.create_TAAS()
        self.create_MVPT()
        self.create_TVAS()
        self.create_MonroeV3()
        
    def count_correct_answers(self):
        """Count the number of correct answers (ticks) for each test type in the status bar"""
        status_text = self.status_text
        
        # Initialize counters
        taas_correct = 0
        tvas_correct = 0
        mvpt_correct = 0
        
        # Count TAAS correct answers (words with check marks)
        taas_words = ["(cow)boy", "steam(boat)", "sun(shine)", "(pic)nic", "(cu)cumber", "(c)oat",
                    "(m)eat", "(t)ake", "(ga)me", "(wro)te", "plea(se)", "(c)lap", "(p)lay", 
                    "s(t)ale", "s(m)ack"]
        
        for word in taas_words:
            # Check if word has a check mark in status
            if f"{word} \u2713" in status_text:
                taas_correct += 1
        
        # Count TVAS correct answers (numbers with check marks)
        for i in range(1, 15):  # TVAS has numbers 1-14
            if f"{i} \u2713" in status_text:
                tvas_correct += 1
        
        # Count MVPT correct answers (numbers with check marks)
        for i in range(1, 37):  # MVPT has numbers 1-36
            if f"{i} \u2713" in status_text:
                mvpt_correct += 1
        
        return taas_correct, tvas_correct, mvpt_correct

    " note: may rewrite this using dict"
    def determine_level(self, test_type, correct_count):
        """Determine the level based on the test type and correct count"""
        if test_type == "TAAS":
            if correct_count <= 2:
                return "pre prep"
            elif correct_count <= 3:
                return "prep"
            elif correct_count <= 6:
                return "Early grade 1"
            elif correct_count <= 9:
                return "Grade 1"
            elif correct_count <= 12:
                return "Early grade 2"
            elif correct_count == 13:
                return "Grade 2"
            elif correct_count == 14:
                return "Early grade 3"
            else:
                return "Grade 3"
            
        elif test_type == "TVAS":
            if correct_count == 1:
                return "pre kinda"
            elif correct_count <= 5:
                return "kinda"
            elif correct_count <= 7:
                return "prep"
            elif correct_count == 8:
                return "Grade 1"
            elif correct_count == 9:
                return "Grade 2"
            elif correct_count == 10:
                return "Grade 3"
            elif correct_count == 12:
                return "Grade 4"
            else:
                return "> Grade 4"
        else:
            return ""  # For MVPT, we just return the count

    def display_scores(self):
        """Calculate and display the scores for each test type"""
        # Count correct answers
        taas_correct, tvas_correct, mvpt_correct = self.count_correct_answers()
        
        # Determine levels
        taas_level = self.determine_level("TAAS", taas_correct)
        tvas_level = self.determine_level("TVAS", tvas_correct)
        
        # Create score message
        score_message = (
            f"\nScores: "
            f"TAAS: {taas_correct}/15 ({taas_level}), "
            f"TVAS: {tvas_correct}/14 ({tvas_level}), "
            f"MVPT Total = {mvpt_correct}/36"
        )
        
        # Update status bar with score
        self.update_status(score_message)

    def toggle_state(self, checkbox, state_var, label, prefix=None, word=None):
        # Cycle through states: 0 -> 1 -> 2 -> 0
        current_state = int(state_var.get())
        next_state = (current_state + 1) % 3
        
        state_var.set(str(next_state))
        
        # Update checkbox appearance based on state
        if next_state == 0:  # Off state - remove from status
            checkbox.deselect()
            checkbox.configure(fg_color=ctk.ThemeManager.theme["CTkCheckBox"]["fg_color"])
            checkbox.configure(hover_color=ctk.ThemeManager.theme["CTkCheckBox"]["hover_color"])
            
            # Remove the label from status
            self.remove_status_label(label)
            
        elif next_state == 1:  # On with green (check mark)
            checkbox.select()
            checkbox.configure(fg_color="green", hover_color="#006400")
            
            # Determine the text to add to status
            text_to_add = ""
            # Handle prefix for first button if needed
            if prefix and ((prefix == "TAAS" and not self.first_taas_clicked) or 
                        (prefix == "MVPT" and not self.first_mvpt_clicked) or 
                        (prefix == "TVAS" and not self.first_tvas_clicked)):
                text_to_add = prefix + " "
                if prefix == "TAAS":
                    self.first_taas_clicked = True
                elif prefix == "MVPT":
                    self.first_mvpt_clicked = True
                elif prefix == "TVAS":
                    self.first_tvas_clicked = True
            
            # Add the text to display
            if word:
                text_to_add += word
            else:
                text_to_add += label
                
            # Add check mark to display
            display_text = f"{text_to_add} \u2713"
            self.update_status(display_text)
            self.status_labels[label] = "\u2713"  # Check mark
            
        elif next_state == 2:  # On with red (cross mark)
            checkbox.select()
            checkbox.configure(fg_color="red", hover_color="#8B0000")
            
            # Find and replace the check mark with a cross mark
            if label in self.status_labels:
                # Save current status to history for undo
                self.status_history.append(self.status_text)
                
                # Create search text with check mark
                search_text = ""
                if word:
                    search_text = f"{word} \u2713"
                else:
                    search_text = f"{label} \u2713"
                    
                # Create replacement text with cross mark
                replace_text = ""
                if word:
                    replace_text = f"{word} \u2717"
                else:
                    replace_text = f"{label} \u2717"
                
                # Replace in the status text
                self.status_text = self.status_text.replace(search_text, replace_text)
                self.status_textbox.delete(1.0, "end")
                self.status_textbox.insert("end", self.status_text)
                
                # Update the stored symbol
                self.status_labels[label] = "\u2717"  # Cross mark
    
    def update_status_label(self, label, symbol):
        if label in self.status_labels:
            # Already in status bar, update the symbol
            old_text = f"{label} {self.status_labels[label]}"
            new_text = f"{label} {symbol}"
            
            # Save current status to history for undo
            self.status_history.append(self.status_text)
            
            # Update the text in the status bar
            self.status_text = self.status_text.replace(old_text, new_text)
            self.status_textbox.delete(1.0, "end")
            self.status_textbox.insert("end", self.status_text)
            
            # Update the stored symbol
            self.status_labels[label] = symbol
        else:
            # Not in status bar yet, add it
            self.status_labels[label] = symbol
            
            # Add to status bar
            self.update_status(f"{label} {symbol}")
    
    def remove_status_label(self, label):
        if label in self.status_labels:
            # Save current status to history for undo
            self.status_history.append(self.status_text)
            
            # Determine the text to remove
            text_to_remove = ""
            symbol = self.status_labels[label]
            
            # Check different patterns - with and without NG
            patterns_to_check = [
                f"{label} {symbol}",
                f"{label} {symbol} NG"
            ]
            
            # Try to find the exact pattern in the status text
            for pattern in patterns_to_check:
                if pattern in self.status_text:
                    text_to_remove = pattern
                    break
            
            # If found, remove it
            if text_to_remove and text_to_remove in self.status_text:
                # If preceded by space
                if f" {text_to_remove}" in self.status_text:
                    self.status_text = self.status_text.replace(f" {text_to_remove}", "")
                # If at the beginning or standalone
                else:
                    self.status_text = self.status_text.replace(text_to_remove, "")
                    
                # Clean up any extra spaces
                self.status_text = self.status_text.strip()
                
                # Update the textbox
                self.status_textbox.delete(1.0, "end")
                self.status_textbox.insert("end", self.status_text)
            
            # Remove from our tracking dictionary
            if label in self.status_labels:
                del self.status_labels[label]
    
    def create_main_content(self):
        # Left column
        left_frame = ctk.CTkFrame(self.main_frame, fg_color="#c2e6c2", corner_radius=0, width=70)
        left_frame.pack(side="left", fill="y", expand=False)
        
        # DEM sections
        self.dem_entries = {}  # Store entries for reference
        dem_labels = ["DEM A", "DEM B", "DEM C", "Skip line", "Rpt line"]
        
        for label in dem_labels:
            frame = ctk.CTkFrame(left_frame, fg_color="#c2e6c2", corner_radius=0, height=30)
            frame.pack(fill="x", pady=2)
            
            # Modify the command for each button - removed status updates
            if label in ["DEM A", "DEM B", "DEM C"]:
                label_button = ctk.CTkButton(frame, text=label, fg_color="#f0f0f0", text_color="black", 
                                             hover_color="#e0e0e0", corner_radius=5, height=25, width=80,
                                             command=lambda l=label: self.toggle_increment_timer(l))
                
            elif label in ["Skip line", "Rpt line"]:
                label_button = ctk.CTkButton(frame, text=label, fg_color="#f0f0f0", 
                                             text_color="black", hover_color="#e0e0e0", 
                                             corner_radius=5, height=25, width=80,
                                             command=lambda l=label: self.increment_entry(l))
                
            else:
                label_button = ctk.CTkButton(frame, text=label, fg_color="#f0f0f0", 
                                             text_color="black", hover_color="#e0e0e0", 
                                             corner_radius=5, height=25, width=80)
                
            label_button.pack(side="left", padx=5)
            
            entry = ctk.CTkEntry(frame, width=50, height=25, border_width=1)
            entry.pack(side="left", padx=10)
            entry.insert(0, "0")
            
            # Store entries in dictionary for later access
            self.dem_entries[label] = entry
        
        # Radio buttons
        radio_frame = ctk.CTkFrame(left_frame, width=40, fg_color="#c2e6c2", corner_radius=0)
        radio_frame.pack(pady=5)
        
        radio_label = ctk.CTkLabel(radio_frame, text="Put on")
        radio_label.pack(side="left", padx=5)
        
        radio_var = tk.StringVar(value="+0.5")
        radio1 = ctk.CTkRadioButton(radio_frame, text="+0.5", variable=radio_var, value="+0.5", width=10,
                                   command=lambda: self.update_status("+0.50 RX"))
        radio1.pack(side="left", padx=5)
        
        radio2 = ctk.CTkRadioButton(radio_frame, text="+0.75", variable=radio_var, value="+0.75", width=10,
                                   command=lambda: self.update_status("+0.75 RX"))
        radio2.pack(side="left", padx=5)
        
        radio3 = ctk.CTkRadioButton(radio_frame, text="+1.00", variable=radio_var, value="+1.00", width=10,
                                   command=lambda: self.update_status("+1.00 RX"))
        radio3.pack(side="left", padx=5)
        
        button_frame = ctk.CTkFrame(left_frame, fg_color="#c2e6c2", corner_radius=0)
        button_frame.pack(pady=10)
        
        self.done_button = ctk.CTkButton(button_frame, text="Done", 
                                         fg_color="#4CAF50", text_color="white", 
                                         width=100, height=30,
                                         command=self.calculate_dem_results)
        self.done_button.pack(fill="x", pady=5)
        
        self.new_line_button = ctk.CTkButton(button_frame, text="New Line", fg_color="#E090E0",
                                             text_color="black", width=100, height=30,
                                             command=self.new_line)
        self.new_line_button.pack(fill="x", pady=5)
        
        monitor_btn = ctk.CTkButton(button_frame, text="Monroe V3", fg_color="#6699ff", 
                                    hover_color="#4d88ff", corner_radius=5, height=30,
                                    command=lambda: self.update_status("Monroe V3"))
        monitor_btn.pack(fill="x", pady=5)
        
    def create_control_buttons(self):
        self.button_frame = ctk.CTkFrame(self, fg_color="#c2e6c2", corner_radius=0)
        self.button_frame.place(x=450, y=200)
        
        self.undo_button = ctk.CTkButton(self.button_frame, text="Undo", 
                                        fg_color="#A52A2A", text_color="white", width=100, height=40,
                                        command=self.undo_status)
        self.undo_button.pack(pady=5)
        
        self.clear_status_button = ctk.CTkButton(self.button_frame, text="Clear Status", 
                                                fg_color="#FF4500", text_color="white", 
                                                width=100, height=30, command=self.clear_status)
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
        
        # Add the new Calculate Scores button
        self.score_button = ctk.CTkButton(
            self.button_frame,
            text="Calculate Scores",
            fg_color="#4169E1",  # Royal Blue
            text_color="white",
            width=110,
            height=40,
            command=self.display_scores
        )
        self.score_button.pack(pady=5)
    
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
                f"DEM A = {dem_a} sec, "
                f"DEM B = {dem_b} sec, "
                f"DEM A + DEM B = {dem_ab_total} sec, "
                f"DEM C = {dem_c} sec, "
                f"Skip lines: {skip_lines} sec, "
                f"Rpt lines: {rpt_lines} sec, "
                f"Total = {total} sec"
            )
            self.update_status(results_message)
            
        except ValueError:
            self.update_status("Error: All DEM values must be numbers")
    
    def create_TAAS(self):
        self.TAAS_frame = ctk.CTkFrame(self.main_frame, width=130, height=180, fg_color="white", corner_radius=5)
        self.TAAS_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.TAAS_frame.pack_propagate(False)  # This prevents the frame from shrinking
        
        self.TAAS_label = ctk.CTkLabel(self.TAAS_frame, text="TAAS")
        self.TAAS_label.pack(fill="x", padx=5, pady=5)

        wordlist = ["(cow)boy", "steam(boat)", "sun(shine)", "(pic)nic", "(cu)cumber", "(c)oat",
                    "(m)eat", "(t)ake", "(ga)me", "(wro)te", "plea(se)", "(c)lap", "(p)lay", 
                    "s(t)ale", "s(m)ack"]
        
        # Find the index of "sun(shine)" to start numbering from
        sunshine_index = wordlist.index("sun(shine)")
        
        # Create checkboxes for each word
        self.taas_checkboxes = []
        self.taas_state_vars = []  # To track the state of each checkbox
        
        for i, word in enumerate(wordlist):
            checkbox_frame = ctk.CTkFrame(self.TAAS_frame, fg_color="transparent")
            checkbox_frame.pack(fill="x", padx=5, pady=2)
            
            # If the word is "sun(shine)" or after, add numbering
            if i >= sunshine_index:
                number = i - sunshine_index + 1  # Start numbering from 1
                display_text = f"{number}. {word}"
            else:
                # For words before "sun(shine)", no numbering
                display_text = word
            
            # Create a StringVar for the checkbox state (0, 1, 2)
            state_var = ctk.StringVar(value="0")
            
            # Create the checkbox
            checkbox = ctk.CTkCheckBox(checkbox_frame, text=display_text, 
                                      onvalue="1", offvalue="0")
            checkbox.pack(side="left", padx=5)
            
            # For the first word, add prefix TAAS
            is_first = (i == 0)
            prefix = "TAAS" if is_first else None
            
            # Configure the checkbox command to use our toggle state function with word as label
            checkbox.configure(command=lambda cb=checkbox, sv=state_var, w=word, p=prefix: 
                               self.toggle_state(cb, sv, w, prefix=p, word=w))
            
            # Store references for later
            self.taas_checkboxes.append(checkbox)
            self.taas_state_vars.append(state_var)

    def create_MVPT(self):
        self.MVPT_frame = ctk.CTkFrame(self.main_frame, width=240, height=180, fg_color="white", corner_radius=5)
        self.MVPT_frame.pack(side="right", fill="y", padx=10, pady=10)
        self.MVPT_frame.pack_propagate(False)  # This prevents the frame from shrinking
        
        self.MVPT_label = ctk.CTkLabel(self.MVPT_frame, text="MVPT")
        self.MVPT_label.pack(fill="x", padx=5, pady=5)
        
        # Create container for the columns
        checkbox_container = ctk.CTkFrame(self.MVPT_frame, fg_color="transparent")
        checkbox_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create three columns
        left_column = ctk.CTkFrame(checkbox_container, fg_color="transparent")
        left_column.pack(side="left", fill="both", expand=True)
        
        middle_column = ctk.CTkFrame(checkbox_container, fg_color="transparent")
        middle_column.pack(side="left", fill="both", expand=True)
        
        right_column = ctk.CTkFrame(checkbox_container, fg_color="transparent")
        right_column.pack(side="left", fill="both", expand=True)
        
        # Store all checkboxes
        self.MVPT_checkboxes = []
        self.MVPT_state_vars = []  # To track the state of each checkbox
        
        # First column (1-12)
        for i in range(1, 13):
            display_text = str(i)
            state_var = ctk.StringVar(value="0")
            
            checkbox = ctk.CTkCheckBox(left_column, text=display_text, width=20, 
                                    onvalue="1", offvalue="0")
            checkbox.pack(anchor="w", padx=5, pady=1)
            
            # Add prefix only to first checkbox
            prefix = "MVPT" if i == 1 else None
            
            # Configure the checkbox command to use our toggle state function
            checkbox.configure(command=lambda cb=checkbox, sv=state_var, num=i, p=prefix: 
                            self.toggle_state(cb, sv, str(num), prefix=p))
            
            # Store references for later
            self.MVPT_checkboxes.append(checkbox)
            self.MVPT_state_vars.append(state_var)
        
        # Second column (13-24)
        for i in range(13, 25):
            display_text = str(i)
            state_var = ctk.StringVar(value="0")
            
            checkbox = ctk.CTkCheckBox(middle_column, text=display_text, width=20,
                                    onvalue="1", offvalue="0")
            checkbox.pack(anchor="w", padx=5, pady=1)
            
            # Configure the checkbox command
            checkbox.configure(command=lambda cb=checkbox, sv=state_var, num=i: 
                            self.toggle_state(cb, sv, str(num)))
            
            # Store references for later
            self.MVPT_checkboxes.append(checkbox)
            self.MVPT_state_vars.append(state_var)
        
        # Third column (25-36)
        for i in range(25, 37):
            display_text = str(i)
            state_var = ctk.StringVar(value="0")
            
            checkbox = ctk.CTkCheckBox(right_column, text=display_text, width=20,
                                    onvalue="1", offvalue="0")
            checkbox.pack(anchor="w", padx=5, pady=1)
            
            # Configure the checkbox command
            checkbox.configure(command=lambda cb=checkbox, sv=state_var, num=i: 
                            self.toggle_state(cb, sv, str(num)))
            
            # Store references for later
            self.MVPT_checkboxes.append(checkbox)
            self.MVPT_state_vars.append(state_var)

    def create_TVAS(self):
        self.TVAS_frame = ctk.CTkFrame(self.main_frame, width=130, height=180, fg_color="white", corner_radius=5)
        self.TVAS_frame.pack(side="right", fill="y", padx=10, pady=10)
        self.TVAS_frame.pack_propagate(False)  # This prevents the frame from shrinking
        
        # Create a header frame to hold both labels
        header_frame = ctk.CTkFrame(self.TVAS_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=5, pady=5)
        
        # Add TVAS label
        self.TVAS_label = ctk.CTkLabel(header_frame, text="TVAS")
        self.TVAS_label.pack(side="left", padx=5)
        
        # Add NG label next to TVAS label
        self.NG_label = ctk.CTkLabel(header_frame, text="NG")
        self.NG_label.pack(side="right", padx=5)
        
        # Store all checkboxes and variables
        self.TVAS_checkboxes = []
        self.TVAS_state_vars = []  # To track the state of each checkbox
        
        self.TVAS_ng_checkboxes = []
        self.TVAS_ng_state_vars = []  # To track the state of each NG checkbox
        
        # Create two columns of checkboxes: numbered 1-14 and NG
        for i in range(1, 15):
            # Create a frame for each row to hold both checkboxes
            row_frame = ctk.CTkFrame(self.TVAS_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=5, pady=2)
            
            # First column: Numbered checkboxes
            display_text = str(i)
            state_var1 = ctk.StringVar(value="0")
            
            checkbox1 = ctk.CTkCheckBox(row_frame, text=display_text, width=50,
                                    onvalue="1", offvalue="0")
            checkbox1.pack(side="left", padx=5)
            
            # Add TVAS prefix only to first checkbox (FIXED: was using MVPT)
            prefix = "TVAS" if i == 1 else None
            
            # Configure the checkbox command
            checkbox1.configure(command=lambda cb=checkbox1, sv=state_var1, num=i, p=prefix: 
                                self.toggle_state(cb, sv, str(num), prefix=p))
            
            # Store references for later
            self.TVAS_checkboxes.append(checkbox1)
            self.TVAS_state_vars.append(state_var1)
            
            # Second column: NG checkboxes - Modified to only have two states
            ng_var = tk.BooleanVar(value=False)
            
            ng_checkbox = ctk.CTkCheckBox(row_frame, text="", 
                                    variable=ng_var, onvalue=True, offvalue=False)
            ng_checkbox.pack(side="right", padx=5)
            
            # Store the current item number for this row
            current_number = i
            
            # Configure special handling for NG checkboxes with only two states
            ng_checkbox.configure(command=lambda cb=ng_checkbox, var=ng_var, num=current_number: 
                                self.toggle_ng(cb, var, num))
            
            # Store references for later
            self.TVAS_ng_checkboxes.append(ng_checkbox)
            self.TVAS_ng_state_vars.append(ng_var)

    # Add a new function to handle NG checkbox states
    def toggle_ng(self, checkbox, state_var, number):
        # Get the label (number) that this NG checkbox is associated with
        label = str(number)
        
        # Check if checkbox is now selected or deselected
        if state_var.get():  # If checked
            # Check if the number is already in the status bar
            found = False
            for word in self.status_text.split():
                if word == label:
                    found = True
                    break
                    
            if found:
                # Save current status to history for undo
                self.status_history.append(self.status_text)
                
                # Look for the pattern "number checkmark" or "number crossmark"
                search_patterns = [f"{label} \u2713", f"{label} \u2717"]
                for pattern in search_patterns:
                    if pattern in self.status_text:
                        # Replace with pattern + NG
                        self.status_text = self.status_text.replace(pattern, f"{pattern} NG")
                        break
                
                # Update the textbox
                self.status_textbox.delete(1.0, "end")
                self.status_textbox.insert("end", self.status_text)
            else:
                # If the number isn't in status yet, add it with NG
                self.update_status(f"{label} NG")
        else:  # If unchecked
            # Remove "NG" from the status text if it's there
            # Save current status to history for undo
            self.status_history.append(self.status_text)
            
            # Look for patterns with NG
            search_patterns = [f"{label} \u2713 NG", f"{label} \u2717 NG"]
            for pattern in search_patterns:
                if pattern in self.status_text:
                    # Replace with pattern without NG
                    self.status_text = self.status_text.replace(pattern, pattern[:-3])
                    break
            
            # Also check for just "{label} NG"
            if f"{label} NG" in self.status_text:
                self.status_text = self.status_text.replace(f"{label} NG", label)
            
            # Update the textbox
            self.status_textbox.delete(1.0, "end")
            self.status_textbox.insert("end", self.status_text)

    def create_MonroeV3(self):
        pass    

    def toggle_increment_timer(self, label):
        # Check if timer is already running
        if label in self.timer_ids and self.timer_ids[label]:
            # Stop the timer
            self.after_cancel(self.timer_ids[label])
            self.timer_ids[label] = None
        else:
            # Start the timer
            self.increment_entry_with_timer(label)
    
    def increment_entry_with_timer(self, label):
        # Get current value
        entry = self.dem_entries[label]
        current_value = int(entry.get())
        
        # Increment the value
        entry.delete(0, 'end')
        entry.insert(0, str(current_value + 1))
        
        # Schedule next increment
        self.timer_ids[label] = self.after(1000, lambda: self.increment_entry_with_timer(label))
    
    def increment_entry(self, label):
        entry = self.dem_entries[label]
        current_value = int(entry.get())
        
        # Increment the value
        entry.delete(0, 'end')
        entry.insert(0, str(current_value + 1))
    
    # Functions for handling status updates
    def update_status(self, text):
        # Save current status to history for undo
        self.status_history.append(self.status_text)
        
        # Add a space before the new text if the current text is not empty and doesn't end with space
        separator = " " if self.status_text and not self.status_text.endswith(" ") else ""
        self.status_text += separator + text
        
        # Update the textbox
        self.status_textbox.delete(1.0, "end")
        self.status_textbox.insert("end", self.status_text)
        self.status_textbox.see("end")

    def new_line(self):
        # Save current status to history for undo
        self.status_history.append(self.status_text)
        self.status_text += "\n"
        self.status_textbox.delete(1.0, "end")
        self.status_textbox.insert("end", self.status_text)
        self.status_textbox.see("end")

    def clear_status(self):
        # Save current status to history for undo
        self.status_history.append(self.status_text)
        self.status_text = ""
        self.status_textbox.delete(1.0, "end")
        
        # Also clear the status labels dictionary
        self.status_labels = {}

    def undo_status(self):
        if self.status_history:
            # Reset the status labels dictionary by parsing the previous status text
            # This is a simplified approach and might not perfectly restore the state
            self.status_text = self.status_history.pop()
            self.status_textbox.delete(1.0, "end")
            self.status_textbox.insert("end", self.status_text)
            self.status_textbox.see("end")
            
            # Reset the status labels tracking
            self.status_labels = {}
            
            # Check if we need to reset the first_clicked flags
            self.first_taas_clicked = "TAAS" in self.status_text
            self.first_tvas_clicked = "TVAS" in self.status_text
            self.first_mvpt_clicked = "MVPT" in self.status_text
            
            # Simple parsing to restore status labels
            for test_type in ["MVPT", "TAAS", "TVAS"]:
                for item in self.status_text.split():
                    if item.startswith(test_type):
                        # Extract the label and symbol
                        parts = item.split()
                        if len(parts) > 1:
                            label = parts[0]
                            if "\u2713" in self.status_text or "\u2717" in self.status_text:
                                symbol = "\u2713" if "\u2713" in self.status_text else "\u2717"
                                self.status_labels[label] = symbol    

    def copy_all(self):
        # Updated to match Binocular.txt implementation
        pyperclip.copy(self.status_textbox.get(1.0, "end-1c"))

if __name__ == "__main__":
    app = Perceptual()
    app.mainloop()