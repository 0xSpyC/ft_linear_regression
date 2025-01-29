import tkinter as tk
import threading
from tkinter import ttk
from .views import TrainingView
from .model import TrainingParameters
from .model_trainer import ModelTrainer
from .config import *

class TrainingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Program")
        self.root.geometry("800x300")
        self.root.resizable(False, False)
        
        self.parameters = TrainingParameters()
        self.parameters.load_initial_parameters()
        
        self.view = TrainingView(self.root)
        self.view.pack(fill=tk.BOTH, expand=True)  
        self.view.set_commands(
            self.start_training,
            self.stop_training,
            self.reset_training
        )
        
        self.trainer = None
        self.training_thread = None

    def start_training(self):
        if not self.trainer or not self.trainer.training_active:
            learning_rate = self.view.get_learning_rate()
            self.trainer = ModelTrainer(
                self.parameters,
                float(learning_rate),
                lambda: self.root.after(0, self.update_ui)
            )
            self.training_thread = threading.Thread(
                target=self.trainer.run, 
                daemon=True
            )
            self.training_thread.start()

    def stop_training(self):
        if self.trainer:
            self.trainer.stop()

    def reset_training(self):
        self.parameters.reset()
        self.reset_ui()

    def update_ui(self):
        theta0, theta1 = self.parameters.denormalized_parameters
        self.view.update_theta_labels(theta0, theta1)

    def reset_ui(self):
        theta0, theta1 = (0,0)
        self.view.update_theta_labels(theta0, theta1)
    
    

def main():

    root = tk.Tk()
    app = TrainingApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
