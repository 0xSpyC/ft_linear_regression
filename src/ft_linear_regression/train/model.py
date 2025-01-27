import numpy as np
from ..utils.data_utils import (
    load_parameters_from_json,
    load_normalized_data,
    modify_json_parameters,
    denormalize_parameters
)

class TrainingParameters:
    def __init__(self):
        self.theta0 = 0.0
        self.theta1 = 0.0
        self.loss = np.array([])
        self.normalized_data = None

    def load_initial_parameters(self):
        parameters = load_parameters_from_json()
        self.theta0 = parameters.theta0
        self.theta1 = parameters.theta1
        self.loss = parameters.loss
        self.normalized_data = load_normalized_data()

    @property
    def denormalized_parameters(self):
        return denormalize_parameters(
            self.theta0, 
            self.theta1, 
            self.normalized_data
        )

    def save(self):
        theta0, theta1 = self.denormalized_parameters
        modify_json_parameters(theta0, theta1, self.loss.tolist())

    def reset(self):
        self.theta0 = 0.0
        self.theta1 = 0.0
        self.loss = np.array([])
        modify_json_parameters(self.theta0, self.theta1, self.loss.tolist())