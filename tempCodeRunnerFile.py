    self.button_frame = ctk.CTkFrame(self, fg_color="#c2e6c2", corner_radius=0)
        self.button_frame.place(x=60, y=400)
        
        self.undo_button = ctk.CTkButton(self.button_frame, text="Undo", 
                                        fg_color="#A52A2A", text_color="white", width=100, height=40,
                                        command=self.undo_status)
        self.undo_button.pack(pady=5)
        
        self.clear_status_button = ctk.CTkButton(self.button_frame, text="Clear Status", 
                                                fg_color="#FF4500", text_color="white", 
                                                width=100, height=30, command=self.clear_status)
        self.clear_status_button.pack(pady=5)
        
        # Add a button to manually update scores if needed
        self.update_scores_button = ctk.CTkButton(
            self.button_frame, 
            text="Update Scores", 
            fg_color="#4682B4", 
            text_color="white", 
            width=110, 
            height=30,
            command=self.update_score_section
        )
        self.update_scores_button.pack(pady=5)
        
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