from tkinter import ttk

class TrainingView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        
    def create_widgets(self):
        self.theta0_label = ttk.Label(self, text="Theta 0: 0.0000", width=20)
        self.theta0_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.theta1_label = ttk.Label(self, text="Theta 1: 0.0000", width=20)
        self.theta1_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.learning_rate_label = ttk.Label(self, text="Learning Rate:")
        self.learning_rate_label.grid(row=2, column=0, padx=10, pady=10)
        
        self.learning_rate_entry = ttk.Entry(self)
        self.learning_rate_entry.insert(0, "0.1")
        self.learning_rate_entry.grid(row=2, column=1, padx=10, pady=10)
        
        self.start_button = ttk.Button(self, text="Start Training")
        self.start_button.grid(row=3, column=0, padx=10, pady=10)
        
        self.stop_button = ttk.Button(self, text="Stop Training")
        self.stop_button.grid(row=3, column=1, padx=10, pady=10)
        
        self.reset_button = ttk.Button(self, text="Reset Training")
        self.reset_button.grid(row=3, column=2, padx=10, pady=10)

    def update_theta_labels(self, theta0, theta1):
        self.theta0_label.config(text=f"Theta 0: {theta0:.4f}")
        self.theta1_label.config(text=f"Theta 1: {theta1:.4f}")

    def get_learning_rate(self):
        return self.learning_rate_entry.get()

    def set_commands(self, start_cmd, stop_cmd, reset_cmd):
        self.start_button.config(command=start_cmd)
        self.stop_button.config(command=stop_cmd)
        self.reset_button.config(command=reset_cmd)