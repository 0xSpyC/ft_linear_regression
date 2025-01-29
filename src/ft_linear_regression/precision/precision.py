import numpy as np
from ..utils.data_utils import load_parameters_from_json, load_normalized_data


RED_BOLD = "\033[1;33m"
RESET = "\033[0m"


def apply_affine(x, theta0, theta1):
    y = theta1 * x + theta0
    return y

def r2_score(y_true, y_pred):
    ss_total = np.sum((y_true - np.mean(y_true)) ** 2)
    ss_residual = np.sum((y_true - y_pred) ** 2)
    
    r2 = 1 - (ss_residual / ss_total) if ss_total != 0 else 0
    return max(0, r2)

def main():
    parameters = load_parameters_from_json()
    data = load_normalized_data()

    y_pred = apply_affine(data["km"], parameters.theta0, parameters.theta1)
    y_true = data["price"]

    r2 = r2_score(y_true, y_pred)

    print(f"{RED_BOLD}The precision of the algorithm is {r2 * 100} %{RESET}")
    



if __name__ == "__main__":
    main()