import time
import numpy as np

class ModelTrainer:
    def __init__(self, parameters, learning_rate, update_callback=None):
        self.parameters = parameters
        self.learning_rate = learning_rate
        self.update_callback = update_callback
        self.training_active = False

    def run(self):
        self.training_active = True
        while self.training_active:
            self.train_step()
            time.sleep(0.2)

    def train_step(self):
        data = self.parameters.normalized_data
        x = data["x_normalized"]
        y = data["y_normalized"]
        m = len(x)

        estimated_price = self.parameters.theta0 + self.parameters.theta1 * x
        errors = estimated_price - y
        grad0 = (1/m) * np.sum(errors)
        grad1 = (1/m) * np.sum(errors * x)

        tmp_theta0 = self.learning_rate * grad0
        tmp_theta1 = self.learning_rate * grad1

        self.parameters.theta0 -= tmp_theta0
        self.parameters.theta1 -= tmp_theta1

        self.update_loss(m)
        self.parameters.save()

        if self.update_callback:
            self.update_callback()

    def update_loss(self, m):
        theta0, theta1 = self.parameters.denormalized_parameters
        km = self.parameters.normalized_data["km"]
        price = self.parameters.normalized_data["price"]
        loss = np.sum((theta0 + theta1 * km - price) ** 2) / m
        self.parameters.loss = np.append(self.parameters.loss, loss)

    def stop(self):
        self.training_active = False