# Configure window
        self.title("Medical Assessment Interface")
        self.geometry("1050x750")
        self.configure(fg_color="#c2e6c2")
        
        # Initialize variables
        self.status_text = ""
        self.status_history = []
        self.status_labels = {}
        self.timer_ids = {"DEM A": None, "DEM B": None, "DEM C": None}  # Initialize with None for each timer
        self.test_first_clicked = {"TAAS": False, "TVAS": False, "MVPT": False}
        
        # Define Monroe V3 level mapping
        self.monroe_levels = {
            (0, -1): "Level 0", (1, 3): "(< age 5)", (4, 5): "(age 5)",   
            (6, 6): "(age 6)", (7, 7): "(age 6.5)", (8, 8): "(age 7)",
            (9, 9): "(age 8)", (10, 10): "(age 9)", (11, 12): "(>= age 10)"
        }
        
        # Test criteria mappings
        self.level_criteria = {
            "TAAS": {
                (0, 2): "pre prep", (3, 3): "prep", (4, 6): "Early grade 1",
                (7, 9): "Grade 1", (10, 12): "Early grade 2", (13, 13): "Grade 2",
                (14, 14): "Early grade 3", (15, 15): "Grade 3"
            },
            "TVAS": {
                (1, 1): "pre kinda", (2, 5): "kinda", (6, 7): "prep",
                (8, 8): "Grade 1", (9, 9): "Grade 2", (10, 10): "Grade 3",
                (11, 12): "Grade 4", (13, 14): "> Grade 4"
            }
        }
        
        # Create UI components
        self.create_status_bar()
        self.create_main_frame()
        self.create_control_buttons()
        
    def create_status_bar(self):
        # Create the status bar frame at the bottom
        self.status_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", height=100)
        self.status_frame.pack(side="bottom", fill="x", padx=5, pady=5)
        self.status_frame.pack_propagate(False)
        
        # Create status textbox inside the status frame
        self.status_textbox = ctk.CTkTextbox(self.status_frame, fg_color="#FFFFFF")
        self.status_textbox.pack(fill="both", expand=True)
        
    def create_main_frame(self):
        # Create the main frame
        self.main_frame = ctk.CTkFrame(self, fg_color="#c2e6c2", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create DEM section (left side)
        self.create_dem_section()
        
        # Create test frames
        self.create_test_frame("TAAS", self.create_TAAS_content, width=150)
        self.create_test_frame("TVAS", self.create_TVAS_content, width=130, side="right")
        self.create_test_frame("MVPT", self.create_MVPT_content, width=240, side="right")
        
    def create_dem_section(self):
        left_frame = ctk.CTkFrame(self.main_frame, fg_color="#c2e6c2", corner_radius=0, width=70)
        left_frame.pack(side="left", fill="y", expand=False)
        
        # DEM sections
        self.dem_entries = {}
        dem_labels = ["DEM A", "DEM B", "DEM C", "Skip line", "Rpt line"]
        
        for label in dem_labels:
            frame = ctk.CTkFrame(left_frame, fg_color="#c2e6c2", corner_radius=0, height=30)
            frame.pack(fill="x", pady=2)
            
            # Create button with appropriate command
            if label in ["DEM A", "DEM B", "DEM C"]:
                # Pass the specific label to the toggle_increment_timer function
                command = lambda l=label: self.toggle_increment_timer(l)
            elif label in ["Skip line", "Rpt line"]:
                command = lambda l=label: self.increment_entry(l)
            else:
                command = None
            
            label_button = ctk.CTkButton(frame, text=label, fg_color="#f0f0f0", text_color="black", 
                                         hover_color="#e0e0e0", corner_radius=5, height=25, width=80,
                                         command=command)
            label_button.pack(side="left", padx=5)
            
            # Create entry field
            entry = ctk.CTkEntry(frame, width=50, height=25, border_width=1)
            entry.pack(side="left", padx=10)
            entry.insert(0, "0")
            self.dem_entries[label] = entry
        
        # Radio buttons for RX
        radio_frame = ctk.CTkFrame(left_frame, width=40, fg_color="#c2e6c2", corner_radius=0)
        radio_frame.pack(pady=5)
        
        radio_label = ctk.CTkLabel(radio_frame, text="Put on")
        radio_label.pack(side="left", padx=5)
        
        radio_var = tk.StringVar(value="+0.5")
        for rx in ["+0.5", "+0.75", "+1.00"]:
            rx_radio = ctk.CTkRadioButton(radio_frame, text=rx, variable=radio_var, value=rx, width=10,
                                       command=lambda v=rx: self.update_status(f"{v} RX"))
            rx_radio.pack(side="left", padx=5)
        
        # Control buttons
        button_frame = ctk.CTkFrame(left_frame, fg_color="#c2e6c2", corner_radius=0)
        button_frame.pack(pady=10)
        
        # Create control buttons
        self.done_button = self.create_button(button_frame, "Done", "#4CAF50", "white", self.calculate_dem_results)
        self.new_line_button = self.create_button(button_frame, "New Line", "#E090E0", "black", self.new_line)
        self.monroe_btn = self.create_button(button_frame, "Monroe V3", "#6699ff", "black", self.submit_monroe_score)
        
        # Monroe score entry
        monroe_entry_frame = ctk.CTkFrame(button_frame, fg_color="#c2e6c2", corner_radius=0)
        monroe_entry_frame.pack(fill="x", pady=2)
        
        entry_label = ctk.CTkLabel(monroe_entry_frame, text="Score:", fg_color="#c2e6c2")
        entry_label.pack(side="left", padx=(10, 5))
        
        self.monroe_score_entry = ctk.CTkEntry(monroe_entry_frame, width=60, height=25, border_width=1)
        self.monroe_score_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.monroe_score_entry.insert(0, "0")
        
    def create_button(self, parent, text, color, text_color, command, width=100, height=30):
        button = ctk.CTkButton(parent, text=text, fg_color=color, text_color=text_color, 
                               width=width, height=height, command=command)
        button.pack(fill="x", pady=5)
        return button
        
    def create_control_buttons(self):
        self.button_frame = ctk.CTkFrame(self, fg_color="#c2e6c2", corner_radius=0)
        self.button_frame.place(x=450, y=200)
        
        buttons = [
            ("Undo", "#A52A2A", "white", self.undo_status, 100, 40),
            ("Clear Status", "#FF4500", "white", self.clear_status, 100, 30),
            ("Copy All", "#A0A000", "black", self.copy_all, 110, 50),
            ("Calculate Scores", "#4169E1", "white", self.display_scores, 110, 40)
        ]
        
        for text, color, text_color, command, width, height in buttons:
            self.create_button(self.button_frame, text, color, text_color, command, width, height)
    
    def create_test_frame(self, title, content_func, width=150, height=180, side="left"):
        frame = ctk.CTkFrame(self.main_frame, width=width, height=height, fg_color="white", corner_radius=5)
        frame.pack(side=side, fill="y", padx=10, pady=10)
        frame.pack_propagate(False)
        
        label = ctk.CTkLabel(frame, text=title, height= 10)
        label.pack(fill="x", padx=5, pady=5)
        
        # Call the content creation function
        content_func(frame, title)
        
        return frame
    
    def create_TAAS_content(self, parent, title):
        wordlist = ["(cow)boy", "steam(boat)", "sun(shine)", "(pic)nic", "(cu)cumber", "(c)oat",
                    "(m)eat", "(t)ake", "(ga)me", "(wro)te", "plea(se)", "(c)lap", "(p)lay", 
                    "s(t)ale", "s(m)ack"]
        
        # Find the index of "sun(shine)" to start numbering from
        sunshine_index = wordlist.index("sun(shine)")
        
        # Create checkboxes for each word
        self.taas_checkboxes = []
        self.taas_state_vars = []
        
        for i, word in enumerate(wordlist):
            checkbox_frame = ctk.CTkFrame(parent, fg_color="transparent")
            checkbox_frame.pack(fill="x", padx=5, pady=2)
            
            # If the word is "sun(shine)" or after, add numbering
            if i >= sunshine_index:
                number = i - sunshine_index + 1
                display_text = f"{number}. {word}"
            else:
                display_text = word
            
            state_var = ctk.StringVar(value="0")
            checkbox = ctk.CTkCheckBox(checkbox_frame, text=display_text, onvalue="1", offvalue="0")
            checkbox.pack(side="left", padx=5)
            
            is_first = (i == 0)
            prefix = title if is_first else None
            
            checkbox.configure(command=lambda cb=checkbox, sv=state_var, w=word, p=prefix: 
                               self.toggle_state(cb, sv, w, prefix=p, word=w))
            
            self.taas_checkboxes.append(checkbox)
            self.taas_state_vars.append(state_var)
    
    def create_MVPT_content(self, parent, title):
        # Create container for the columns
        checkbox_container = ctk.CTkFrame(parent, fg_color="transparent")
        checkbox_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create three columns
        columns = [ctk.CTkFrame(checkbox_container, fg_color="transparent") for _ in range(3)]
        for col in columns:
            col.pack(side="left", fill="both", expand=True)
        
        # Store all checkboxes
        self.MVPT_checkboxes = []
        self.MVPT_state_vars = []
        
        # Create checkboxes in three columns
        ranges = [(1, 13), (13, 25), (25, 37)]
        
        for col_idx, (start, end) in enumerate(ranges):
            for i in range(start, end):
                state_var = ctk.StringVar(value="0")
                checkbox = ctk.CTkCheckBox(columns[col_idx], text=str(i), width=20, 
                                        onvalue="1", offvalue="0")
                checkbox.pack(anchor="w", padx=5, pady=1)
                
                prefix = title if i == 1 else None
                
                checkbox.configure(command=lambda cb=checkbox, sv=state_var, num=i, p=prefix: 
                                self.toggle_state(cb, sv, str(num), prefix=p))
                
                self.MVPT_checkboxes.append(checkbox)
                self.MVPT_state_vars.append(state_var)
    
    def create_TVAS_content(self, parent, title):
        # Create a header frame to hold both labels
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=5, pady=5)
        
        # Add TVAS label
        tvas_label = ctk.CTkLabel(header_frame, text=title, height=10)
        tvas_label.pack(side="left", padx=5)
        
        # Add NG label next to TVAS label
        ng_label = ctk.CTkLabel(header_frame, text="NG", height=10)
        ng_label.pack(side="right", padx=5)
        
        # Store all checkboxes and variables
        self.TVAS_checkboxes = []
        self.TVAS_state_vars = []
        self.TVAS_ng_checkboxes = []
        self.TVAS_ng_state_vars = []
        
        # Create rows with two checkboxes each
        for i in range(1, 15):
            row_frame = ctk.CTkFrame(parent, fg_color="transparent")
            row_frame.pack(fill="x", padx=5, pady=2)
            
            # First column: Numbered checkboxes
            state_var = ctk.StringVar(value="0")
            checkbox = ctk.CTkCheckBox(row_frame, text=str(i), width=50, onvalue="1", offvalue="0")
            checkbox.pack(side="left", padx=5)
            
            prefix = title if i == 1 else None
            
            checkbox.configure(command=lambda cb=checkbox, sv=state_var, num=i, p=prefix: 
                                self.toggle_state(cb, sv, str(num), prefix=p))
            
            self.TVAS_checkboxes.append(checkbox)
            self.TVAS_state_vars.append(state_var)
            
            # Second column: NG checkboxes
            ng_var = tk.BooleanVar(value=False)
            ng_checkbox = ctk.CTkCheckBox(row_frame, text="", variable=ng_var, onvalue=True, offvalue=False)
            ng_checkbox.pack(side="right", padx=5)
            
            ng_checkbox.configure(command=lambda cb=ng_checkbox, var=ng_var, num=i: 
                                self.toggle_ng(cb, var, num))
            
            self.TVAS_ng_checkboxes.append(ng_checkbox)
            self.TVAS_ng_state_vars.append(ng_var)
    
    def toggle_state(self, checkbox, state_var, label, prefix=None, word=None):
        # Cycle through states: 0 -> 1 -> 2 -> 0
        current_state = int(state_var.get())
        next_state = (current_state + 1) % 3
        state_var.set(str(next_state))
        
        if next_state == 0:  # Off state
            checkbox.deselect()
            checkbox.configure(fg_color=ctk.ThemeManager.theme["CTkCheckBox"]["fg_color"])
            checkbox.configure(hover_color=ctk.ThemeManager.theme["CTkCheckBox"]["hover_color"])
            self.remove_status_label(label)
            
        elif next_state == 1:  # Green check mark
            checkbox.select()
            checkbox.configure(fg_color="green", hover_color="#006400")
            
            # Add prefix if this is the first item in a test section
            text_to_add = ""
            if prefix and not self.test_first_clicked.get(prefix, False):
                text_to_add = prefix + " "
                self.test_first_clicked[prefix] = True
            
            # Add the actual item text
            text_to_add += word if word else label
            display_text = f"{text_to_add} \u2713"
            self.update_status(display_text)
            self.status_labels[label] = "\u2713"  # Check mark
            
        elif next_state == 2:  # Red cross mark
            checkbox.select()
            checkbox.configure(fg_color="red", hover_color="#8B0000")
            
            # Replace check mark with cross mark in status
            search_text = f"{word if word else label} \u2713"
            replace_text = f"{word if word else label} \u2717"
            
            self.status_history.append(self.status_text)
            self.status_text = self.status_text.replace(search_text, replace_text)
            self.status_textbox.delete(1.0, "end")
            self.status_textbox.insert("end", self.status_text)
            
            self.status_labels[label] = "\u2717"  # Cross mark
    
    def toggle_ng(self, checkbox, state_var, number):
        label = str(number)
        
        if state_var.get():  # Checked
            found = any(word == label for word in self.status_text.split())
                
            if found:
                self.status_history.append(self.status_text)
                
                # Look for patterns with checkmark or crossmark
                for pattern in [f"{label} \u2713", f"{label} \u2717"]:
                    if pattern in self.status_text:
                        self.status_text = self.status_text.replace(pattern, f"{pattern} NG")
                        break
                
                self.status_textbox.delete(1.0, "end")
                self.status_textbox.insert("end", self.status_text)
            else:
                self.update_status(f"{label} NG")
        else:  # Unchecked
            self.status_history.append(self.status_text)
            
            # Remove NG from various patterns
            patterns = [f"{label} \u2713 NG", f"{label} \u2717 NG", f"{label} NG"]
            for pattern in patterns:
                if pattern in self.status_text:
                    replacement = pattern[:-3] if "NG" in pattern[-3:] else label
                    self.status_text = self.status_text.replace(pattern, replacement)
            
            self.status_textbox.delete(1.0, "end")
            self.status_textbox.insert("end", self.status_text)
    
    def remove_status_label(self, label):
        if label in self.status_labels:
            self.status_history.append(self.status_text)
            symbol = self.status_labels[label]
            
            # Check different patterns
            patterns = [f"{label} {symbol}", f"{label} {symbol} NG"]
            
            for pattern in patterns:
                if pattern in self.status_text:
                    # Remove with preceding space if present
                    if f" {pattern}" in self.status_text:
                        self.status_text = self.status_text.replace(f" {pattern}", "")
                    else:
                        self.status_text = self.status_text.replace(pattern, "")
            
            self.status_text = self.status_text.strip()
            self.status_textbox.delete(1.0, "end")
            self.status_textbox.insert("end", self.status_text)
            
            # Remove from tracking dict
            if label in self.status_labels:
                del self.status_labels[label]
    
    def toggle_increment_timer(self, label):
        # Check if timer for this specific DEM is active
        if self.timer_ids[label]:

            self.after_cancel(self.timer_ids[label])
            self.timer_ids[label] = None
        else:
            self.increment_entry_with_timer(label)
    
    def increment_entry_with_timer(self, label):
        entry = self.dem_entries[label]
        current_value = int(entry.get())
        entry.delete(0, 'end')
        entry.insert(0, str(current_value + 1))
        # Store the timer ID for this specific DEM test
        self.timer_ids[label] = self.after(1000, lambda: self.increment_entry_with_timer(label))
    
    def increment_entry(self, label):
        entry = self.dem_entries[label]
        current_value = int(entry.get())
        entry.delete(0, 'end')
        entry.insert(0, str(current_value + 1))
    
    def update_status(self, text):
        self.status_history.append(self.status_text)
        separator = " " if self.status_text and not self.status_text.endswith(" ") else ""
        self.status_text += separator + text
        self.status_textbox.delete(1.0, "end")
        self.status_textbox.insert("end", self.status_text)
        self.status_textbox.see("end")

    def new_line(self):
        self.status_history.append(self.status_text)
        self.status_text += "\n"
        self.status_textbox.delete(1.0, "end")
        self.status_textbox.insert("end", self.status_text)
        self.status_textbox.see("end")

    def clear_status(self):
        self.status_history.append(self.status_text)
        self.status_text = ""
        self.status_textbox.delete(1.0, "end")
        self.status_labels = {}
        self.test_first_clicked = {k: False for k in self.test_first_clicked}

    def undo_status(self):
        if self.status_history:
            self.status_text = self.status_history.pop()
            self.status_textbox.delete(1.0, "end")
            self.status_textbox.insert("end", self.status_text)
            self.status_textbox.see("end")
            
            # Reset tracking
            self.status_labels = {}
            self.test_first_clicked = {
                "TAAS": "TAAS" in self.status_text,
                "TVAS": "TVAS" in self.status_text,
                "MVPT": "MVPT" in self.status_text
            }

    def copy_all(self):
        pyperclip.copy(self.status_textbox.get(1.0, "end-1c"))
    
    def count_correct_answers(self):
        status_text = self.status_text
        correct_counts = {"TAAS": 0, "TVAS": 0, "MVPT": 0}
        
        # Count TAAS correct answers (words with check marks)
        taas_words = ["(cow)boy", "steam(boat)", "sun(shine)", "(pic)nic", "(cu)cumber", "(c)oat",
                    "(m)eat", "(t)ake", "(ga)me", "(wro)te", "plea(se)", "(c)lap", "(p)lay", 
                    "s(t)ale", "s(m)ack"]
        
        for word in taas_words:
            if f"{word} \u2713" in status_text:
                correct_counts["TAAS"] += 1
        
        # Count TVAS and MVPT correct answers (numbers with check marks)
        for i in range(1, 15):  # TVAS has numbers 1-14
            if f"{i} \u2713" in status_text:
                correct_counts["TVAS"] += 1
        
        for i in range(1, 37):  # MVPT has numbers 1-36
            if f"{i} \u2713" in status_text:
                correct_counts["MVPT"] += 1
        
        return correct_counts
    
    def determine_level(self, test_type, correct_count):
        if test_type not in self.level_criteria:
            return ""
            
        for score_range, level in self.level_criteria[test_type].items():
            min_score, max_score = score_range
            if min_score <= correct_count <= max_score:
                return level
                
        return ""
    
    def display_scores(self):
        correct_counts = self.count_correct_answers()
        
        taas_level = self.determine_level("TAAS", correct_counts["TAAS"])
        tvas_level = self.determine_level("TVAS", correct_counts["TVAS"])
        
        score_message = (
            f"\nScores: "
            f"TAAS: {correct_counts['TAAS']}/15 ({taas_level}), "
            f"TVAS: {correct_counts['TVAS']}/14 ({tvas_level}), "
            f"MVPT Total = {correct_counts['MVPT']}/36"
        )
        
        self.update_status(score_message)
    
    def submit_monroe_score(self):
        try:
            score = int(self.monroe_score_entry.get())
            level = self.determine_monroe_level(score)
            self.update_status(f"Monroe V3 score = {score} {level}")
        except ValueError:
            self.update_status("Error: Monroe V3 score must be a number")
    
    def determine_monroe_level(self, score):
        for score_range, level_name in self.monroe_levels.items():
            min_score, max_score = score_range
            if min_score <= score <= max_score:
                return level_name
        return self.monroe_levels[(0, -1)]
    
    def calculate_dem_results(self):
        try:
            # Stop any active timers when calculating results
            for label, timer_id in self.timer_ids.items():
                if timer_id:
                    self.after_cancel(timer_id)
                    self.timer_ids[label] = None
            
            dem_values = {label: int(entry.get()) for label, entry in self.dem_entries.items()}
            
            dem_ab_total = dem_values["DEM A"] + dem_values["DEM B"]
            total = dem_values["DEM C"] + (4 * dem_values["Skip line"]) - (4 * dem_values["Rpt line"])
            
            results_message = (
                f"DEM A = {dem_values['DEM A']} sec, "
                f"DEM B = {dem_values['DEM B']} sec, "
                f"DEM A + DEM B = {dem_ab_total} sec, "
                f"DEM C = {dem_values['DEM C']} sec, "
                f"Skip lines: {dem_values['Skip line']} sec, "
                f"Rpt lines: {dem_values['Rpt line']} sec, "
                f"Total = {total} sec"
            )
            self.update_status(results_message)
        except ValueError:
            self.update_status("Error: All DEM values must be numbers")
