import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import pyperclip
import datetime
import os

from ControlButtons import ControlButtons as ControlButtons

class Perceptual(ctk.CTkFrame):
    def __init__(self, master, root_app=None):
        ctk.CTkFrame.__init__(self, master, fg_color="#c2e6c2")
        self.root_app = root_app
        
        self.status_labels = {}
        self.timer_ids = {"DEM A": None, "DEM B": None, "DEM C": None}
        self.test_first_clicked = {"TAAS": False, "TVAS": False, "MVPT": False}
        
        # Track item positions and states
        self.taas_items = []
        self.mvpt_items = []
        self.tvas_items = []
        
        # Monroe levels
        self.monroe_levels = {
            (0, -1): "Level 0", (1, 3): "(< age 5)", (4, 5): "(age 5)",   
            (6, 6): "(age 6)", (7, 7): "(age 6.5)", (8, 8): "(age 7)",
            (9, 9): "(age 8)", (10, 10): "(age 9)", (11, 12): "(>= age 10)"
        }
        
        # TAAS and TVAS levels
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
        
        self.create_main_frame()
        self.create_control_buttons()
        
    def update_status(self, text):
        if self.root_app:
            self.root_app.main_update_status(text)  

    def new_line(self):
        if self.root_app:
            self.root_app.main_new_line()  

    def clear_status(self):
        if self.root_app:
            self.root_app.main_clear_status()
            
            # Reset DEM values
            for label in self.dem_entries:
                self.dem_entries[label].delete(0, 'end')
                self.dem_entries[label].insert(0, "0")
            
            # Stop any active timers
            for label, timer_id in self.timer_ids.items():
                if timer_id:
                    self.after_cancel(timer_id)
                    self.timer_ids[label] = None
            
            # Reset all checkboxes
            for checkbox, state_var in zip(self.taas_checkboxes, self.taas_state_vars):
                checkbox.deselect()
                state_var.set("0")
                checkbox.configure(fg_color=ctk.ThemeManager.theme["CTkCheckBox"]["fg_color"])
                checkbox.configure(hover_color=ctk.ThemeManager.theme["CTkCheckBox"]["hover_color"])
            
            for checkbox, state_var in zip(self.MVPT_checkboxes, self.MVPT_state_vars):
                checkbox.deselect()
                state_var.set("0")
                checkbox.configure(fg_color=ctk.ThemeManager.theme["CTkCheckBox"]["fg_color"])
                checkbox.configure(hover_color=ctk.ThemeManager.theme["CTkCheckBox"]["hover_color"])
            
            for checkbox, state_var in zip(self.TVAS_checkboxes, self.TVAS_state_vars):
                checkbox.deselect()
                state_var.set("0")
                checkbox.configure(fg_color=ctk.ThemeManager.theme["CTkCheckBox"]["fg_color"])
                checkbox.configure(hover_color=ctk.ThemeManager.theme["CTkCheckBox"]["hover_color"])
            
            for ng_checkbox, ng_var in zip(self.TVAS_ng_checkboxes, self.TVAS_ng_state_vars):
                ng_checkbox.deselect()
                ng_var.set(False)
            
            # Reset tracking dictionaries
            self.status_labels = {}
            self.test_first_clicked = {k: False for k in self.test_first_clicked}
            
            # Clear ordered item lists
            self.taas_items = []
            self.mvpt_items = []
            self.tvas_items = []

    def undo_status(self):
        if self.root_app:
            self.root_app.main_undo_status()
            self.update_tracking_after_undo()

    def copy_status(self):
        if self.root_app:
            self.root_app.main_copy_status()     

    def update_tracking_after_undo(self):
        self.status_labels = {}
        if self.root_app:
            current_text = self.root_app.status_textbox.get(1.0, "end-1c")
            self.test_first_clicked = {
                "TAAS": "TAAS" in current_text,
                "TVAS": "TVAS" in current_text,
                "MVPT": "MVPT" in current_text
            }
            
            # Reset ordered item lists
            self.taas_items = []
            self.mvpt_items = []
            self.tvas_items = []
            
            self.reconstruct_item_lists_from_text(current_text)

    def reconstruct_item_lists_from_text(self, text):
        # Extract TAAS items
        taas_wordlist = ["(cow)boy", "steam(boat)", "sun(shine)", "(pic)nic", "(cu)cumber", "(c)oat",
                    "(m)eat", "(t)ake", "(ga)me", "(wro)te", "plea(se)", "(c)lap", "(p)lay", 
                    "s(t)ale", "s(m)ack"]
        
        for word in taas_wordlist:
            if f"{word} \u2713" in text or f"{word} \u2717" in text:
                status = "\u2713" if f"{word} \u2713" in text else "\u2717"
                self.taas_items.append((word, status))
                self.status_labels[word] = status
        
        # Extract MVPT items
        for i in range(1, 37):
            if f"{i} \u2713" in text or f"{i} \u2717" in text:
                status = "\u2713" if f"{i} \u2713" in text else "\u2717"
                self.mvpt_items.append((str(i), status))
                self.status_labels[str(i)] = status
        
        # Extract TVAS items
        for i in range(1, 15):
            if f"{i} \u2713" in text or f"{i} \u2717" in text:
                status = "\u2713" if f"{i} \u2713" in text else "\u2717"
                ng_suffix = " NG" if f"{i} {status} NG" in text else ""
                self.tvas_items.append((str(i), status, ng_suffix))
                self.status_labels[str(i)] = status

    def create_main_frame(self):
        # Create the main frame
        self.main_frame = ctk.CTkFrame(self, fg_color="#c2e6c2", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create DEM section (left side)
        self.create_dem_section()
        
        self.create_frame("TAAS", self.create_TAAS_content, width=150)
        self.create_frame("TVAS", self.create_TVAS_content, width=130, side="right")
        self.create_frame("MVPT", self.create_MVPT_content, width=240, side="right")
        
    def create_dem_section(self):
        left_frame = ctk.CTkFrame(self.main_frame, fg_color="#c2e6c2", corner_radius=0, width=70)
        left_frame.pack(side="left", fill="y", expand=False)
        
        # DEM sections
        self.dem_entries = {}
        dem_labels = ["DEM A", "DEM B", "DEM C", "Skip line", "Rpt line"]
        
        for label in dem_labels:
            frame = ctk.CTkFrame(left_frame, fg_color="#c2e6c2", corner_radius=0, height=30)
            frame.pack(fill="x", pady=2)
            
            if label in ["DEM A", "DEM B", "DEM C"]:
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
        for rx in ["+0.50", "+0.75", "+1.00"]:
            rx_radio = ctk.CTkRadioButton(radio_frame, text=rx, variable=radio_var, value=rx, width=10,
                                       command=lambda v=rx: self.update_status(f"w/ {v} rx"))
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
        
        control_buttons = ControlButtons()
        
        command_map = {
            "Undo": self.undo_status,
            "Clear Status": self.clear_status,
            "Copy All": self.copy_status
        }
        
        for text, color, text_color, width, height, y_offset in control_buttons.button_configs:
            command = command_map.get(text)
            self.create_button(self.button_frame, text, color, text_color, command, width, height)
    
    def create_frame(self, title, content_func, width=150, height=180, side="left"):
        frame = ctk.CTkFrame(self.main_frame, width=width, height=height, fg_color="white", corner_radius=5)
        frame.pack(side=side, fill="y", padx=10, pady=10)
        frame.pack_propagate(False)
        
        label = ctk.CTkLabel(frame, text=title, height= 10)
        label.pack(fill="x", padx=5, pady=5)
        
        # Call the content creation function
        content_func(frame, title)
        
        return frame
    
    def create_TAAS_content(self, parent, title):
        self.taas_wordlist = ["(cow)boy", "steam(boat)", "sun(shine)", "(pic)nic", "(cu)cumber", "(c)oat",
                    "(m)eat", "(t)ake", "(ga)me", "(wro)te", "plea(se)", "(c)lap", "(p)lay", 
                    "s(t)ale", "s(m)ack"]
        
        # Find the index of "sun(shine)" to start numbering from
        sunshine_index = self.taas_wordlist.index("sun(shine)")
        
        # Create checkboxes for each word
        self.taas_checkboxes = []
        self.taas_state_vars = []
        
        for i, word in enumerate(self.taas_wordlist):
            checkbox_frame = ctk.CTkFrame(parent, fg_color="transparent")
            checkbox_frame.pack(fill="x", padx=5, pady=2)
            
            # If the word is "sunshine" or after, add numbering
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
            
            # Pass the index for ordering
            checkbox.configure(command=lambda cb=checkbox, sv=state_var, w=word, p=prefix, idx=i: 
                               self.toggle_taas_state(cb, sv, w, p, idx))
            
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
                
                # Pass the numerical value for proper ordering
                checkbox.configure(command=lambda cb=checkbox, sv=state_var, num=i, p=prefix: 
                                self.toggle_mvpt_state(cb, sv, str(num), p, num))
                
                self.MVPT_checkboxes.append(checkbox)
                self.MVPT_state_vars.append(state_var)
    
    def create_TVAS_content(self, parent, title):
        # Create a header frame to hold both labels
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=5, pady=5)
        
        # Add TVAS label
        tvas_label = ctk.CTkLabel(header_frame, text=title, height=10, width=30)
        tvas_label.pack(side="left", padx=5)
        
        # Add NG label next to TVAS label
        ng_label = ctk.CTkLabel(header_frame, text="NG", height=10, width=50)
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
            checkbox = ctk.CTkCheckBox(row_frame, text=str(i), width=60, onvalue="1", offvalue="0")
            checkbox.pack(side="left", padx=5)
            
            prefix = title if i == 1 else None
            
            # Pass the numerical value for proper ordering
            checkbox.configure(command=lambda cb=checkbox, sv=state_var, num=i, p=prefix: 
                                self.toggle_tvas_state(cb, sv, str(num), p, num))
            
            self.TVAS_checkboxes.append(checkbox)
            self.TVAS_state_vars.append(state_var)
            
            # Second column: NG checkboxes
            ng_var = tk.BooleanVar(value=False)
            ng_checkbox = ctk.CTkCheckBox(row_frame, text="", variable=ng_var, onvalue=True, offvalue=False)
            ng_checkbox.pack(side="right", padx=5)
            
            ng_checkbox.configure(command=lambda cb=ng_checkbox, var=ng_var, num=i: 
                                self.toggle_tvas_ng(cb, var, num))
            
            self.TVAS_ng_checkboxes.append(ng_checkbox)
            self.TVAS_ng_state_vars.append(ng_var)
    
    def toggle_taas_state(self, checkbox, state_var, word, prefix=None, index=0):
        current_state = int(state_var.get())
        next_state = (current_state + 1) % 3
        state_var.set(str(next_state))
        
        if next_state == 0:  # Off state
            checkbox.deselect()
            checkbox.configure(fg_color=ctk.ThemeManager.theme["CTkCheckBox"]["fg_color"])
            checkbox.configure(hover_color=ctk.ThemeManager.theme["CTkCheckBox"]["hover_color"])
            self.remove_item_from_display(word, "TAAS")
            
        elif next_state == 1:  # Green check mark
            checkbox.select()
            checkbox.configure(fg_color="green", hover_color="#006400")
            
            # Add to ordered list with check mark
            self.add_item_to_display(word, "\u2713", "TAAS", index)
            
        elif next_state == 2:  # Red cross mark
            checkbox.select()
            checkbox.configure(fg_color="red", hover_color="#8B0000")
            
            # Update status mark in the ordered list
            self.update_item_status(word, "\u2717", "TAAS")
    
    def toggle_mvpt_state(self, checkbox, state_var, label, prefix=None, item_num=0):
        # Cycle through states: 0 -> 1 -> 2 -> 0
        current_state = int(state_var.get())
        next_state = (current_state + 1) % 3
        state_var.set(str(next_state))
        
        if next_state == 0:  # Off state
            checkbox.deselect()
            checkbox.configure(fg_color=ctk.ThemeManager.theme["CTkCheckBox"]["fg_color"])
            checkbox.configure(hover_color=ctk.ThemeManager.theme["CTkCheckBox"]["hover_color"])
            self.remove_item_from_display(label, "MVPT")
            
        elif next_state == 1:  # Green check mark
            checkbox.select()
            checkbox.configure(fg_color="green", hover_color="#006400")
            
            # Add to ordered list with check mark
            self.add_item_to_display(label, "\u2713", "MVPT", item_num)
            
        elif next_state == 2:  # Red cross mark
            checkbox.select()
            checkbox.configure(fg_color="red", hover_color="#8B0000")
            
            # Update status mark in the ordered list
            self.update_item_status(label, "\u2717", "MVPT")
    
    def toggle_tvas_state(self, checkbox, state_var, label, prefix=None, item_num=0):
        # Cycle through states: 0 -> 1 -> 2 -> 0
        current_state = int(state_var.get())
        next_state = (current_state + 1) % 3
        state_var.set(str(next_state))
        
        if next_state == 0:  # Off state
            checkbox.deselect()
            checkbox.configure(fg_color=ctk.ThemeManager.theme["CTkCheckBox"]["fg_color"])
            checkbox.configure(hover_color=ctk.ThemeManager.theme["CTkCheckBox"]["hover_color"])
            self.remove_item_from_display(label, "TVAS")
            
        elif next_state == 1:  # Green check mark
            checkbox.select()
            checkbox.configure(fg_color="green", hover_color="#006400")
            
            # Add to ordered list with check mark
            self.add_item_to_display(label, "\u2713", "TVAS", item_num)
            
        elif next_state == 2:  # Red cross mark
            checkbox.select()
            checkbox.configure(fg_color="red", hover_color="#8B0000")
            
            # Update status mark in the ordered list
            self.update_item_status(label, "\u2717", "TVAS")
    
    def toggle_tvas_ng(self, checkbox, state_var, number):
        label = str(number)
        
        # Find this item in the TVAS list
        for i, item in enumerate(self.tvas_items):
            if item[0] == label:
                # Update the NG status in our ordered list
                status_mark = item[1]  # Keep current status mark (check or cross)
                ng_suffix = " NG" if state_var.get() else ""
                
                # Update item in list
                self.tvas_items[i] = (label, status_mark, ng_suffix)
                
                # Refresh the display
                self.refresh_display()
                return
        
        # Item not found in list but NG was checked - add it as a standalone NG item
        if state_var.get():
            # Find correct position based on item number
            self.add_item_to_display(label, "", "TVAS", number, None, ng_suffix=" NG")
    
    def add_item_to_display(self, item, status, test_type, position, prefix=None, ng_suffix=""):
        # Track item in status labels
        self.status_labels[item] = status
        
        # Get the corresponding list for this test type
        if test_type == "TAAS":
            items_list = self.taas_items
        elif test_type == "MVPT":
            items_list = self.mvpt_items
        elif test_type == "TVAS":
            items_list = self.tvas_items
        else:
            return
        
        # Find insertion position
        if test_type == "TAAS":
            # For TAAS, position is the index in the wordlist
            insert_position = 0
            for i, (existing_item, _) in enumerate(items_list):
                existing_pos = self.taas_wordlist.index(existing_item)
                if position < existing_pos:
                    insert_position = i
                    break
                else:
                    insert_position = i + 1
            
            # Create new item tuple (for TAAS we just need item and status)
            new_item = (item, status)
            
        elif test_type in ["MVPT", "TVAS"]:
            # For MVPT and TVAS, position is the numerical value
            insert_position = 0
            for i, existing_item_tuple in enumerate(items_list):
                existing_item = existing_item_tuple[0]
                existing_pos = int(existing_item)
                if position < existing_pos:
                    insert_position = i
                    break
                else:
                    insert_position = i + 1
            
            # Create new item tuple
            if test_type == "MVPT":
                new_item = (item, status)
            else:  # TVAS
                new_item = (item, status, ng_suffix)
        
        # Insert the item at the correct position
        items_list.insert(insert_position, new_item)
        
        # Refresh the display with prefix if provided
        self.refresh_display(prefix)
    
    def update_item_status(self, item, new_status, test_type):
        # Update item in status labels
        self.status_labels[item] = new_status
        
        # Get the corresponding list for this test type
        if test_type == "TAAS":
            items_list = self.taas_items
        elif test_type == "MVPT":
            items_list = self.mvpt_items
        elif test_type == "TVAS":
            items_list = self.tvas_items
        else:
            return
        
        # Find and update the item
        for i, item_tuple in enumerate(items_list):
            if item_tuple[0] == item:
                if test_type in ["TAAS", "MVPT"]:
                    items_list[i] = (item, new_status)
                elif test_type == "TVAS":
                    # Preserve NG status
                    ng_suffix = item_tuple[2] if len(item_tuple) > 2 else ""
                    items_list[i] = (item, new_status, ng_suffix)
                break
        
        self.refresh_display()
    
    def remove_item_from_display(self, item, test_type):
        # Remove from status labels
        if item in self.status_labels:
            del self.status_labels[item]
        
        # Get the corresponding list for this test type
        if test_type == "TAAS":
            items_list = self.taas_items
        elif test_type == "MVPT":
            items_list = self.mvpt_items
        elif test_type == "TVAS":
            items_list = self.tvas_items
        else:
            return
        
        # Find and remove the item
        for i, item_tuple in enumerate(items_list):
            if item_tuple[0] == item:
                items_list.pop(i)
                break
        
        self.refresh_display()
    
    def refresh_display(self, prefix=None):
        if not self.root_app:
            return
        
        # Clear the current status text
        self.root_app.status_textbox.delete(1.0, "end")
        
        # Rebuild text section by section
        status_text = ""
        
        # Add TAAS items if there are any
        if self.taas_items:
            # Always add the TAAS prefix if there are items
            status_text += "TAAS "
            for item, status in self.taas_items:
                item_text = f"{item} {status}"
                status_text += item_text + " "
            
            # Add TAAS level
            taas_correct = sum(1 for _, status in self.taas_items if status == "\u2713")
            taas_level = self.determine_level("TAAS", taas_correct)
            if taas_level:
                status_text += f"[{taas_level}] "
        
        # Add MVPT items if there are any
        if self.mvpt_items:
            # Always add the MVPT prefix if there are items
            status_text += "MVPT "
            for item, status in self.mvpt_items:
                item_text = f"{item} {status}"
                status_text += item_text + " "
            
            # Add MVPT level
            mvpt_correct = sum(1 for _, status in self.mvpt_items if status == "\u2713")
            status_text += f"[{mvpt_correct}/36] "
        
        # Add TVAS items if there are any
        if self.tvas_items:
            # Always add the TVAS prefix if there are items
            status_text += "TVAS "
            for i, (item, status, *rest) in enumerate(self.tvas_items):
                ng_suffix = rest[0] if rest else ""
                item_text = f"{item} {status}{ng_suffix}"
                status_text += item_text + " "
            
            # Add TVAS level
            tvas_correct = sum(1 for _, status, *_ in self.tvas_items if status == "\u2713")
            tvas_level = self.determine_level("TVAS", tvas_correct)
            if tvas_level:
                status_text += f"[{tvas_level}] "
        
        # Update textbox with the reconstructed text
        self.root_app.status_textbox.insert("end", status_text)
        self.root_app.status_text = status_text
    
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
    
    def copy_all(self):
        if self.root_app:
            self.root_app.main_copy_status()
        else:
            # Fallback if root_app not available
            pyperclip.copy(self.root_app.status_textbox.get(1.0, "end-1c"))
    
    def count_correct_answers(self):
        if not self.root_app:
            return {"TAAS": 0, "TVAS": 0, "MVPT": 0}
            
        status_text = self.root_app.status_textbox.get(1.0, "end-1c")
        correct_counts = {"TAAS": 0, "TVAS": 0, "MVPT": 0}
        
        # Count correct answers from our ordered lists
        for item, status in self.taas_items:
            if status == "\u2713":  # Check mark
                correct_counts["TAAS"] += 1
        
        for item, status in self.mvpt_items:
            if status == "\u2713":  # Check mark
                correct_counts["MVPT"] += 1
        
        for item, status, *rest in self.tvas_items:
            if status == "\u2713":  # Check mark
                correct_counts["TVAS"] += 1
        
        return correct_counts
    
    def determine_level(self, test_type, correct_count):
        if test_type not in self.level_criteria:
            return ""
            
        for score_range, level in self.level_criteria[test_type].items():
            min_score, max_score = score_range
            if min_score <= correct_count <= max_score:
                return level
        
        # Return empty string if no level matches
        return ""
    
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