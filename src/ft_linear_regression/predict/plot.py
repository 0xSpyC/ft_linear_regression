import matplotlib.pyplot as plt
import numpy as np
from ..utils.data_utils import denormalize_parameters, load_parameters_from_json

def linear_regression(parameters, mileage_range=np.linspace(0, 250000, 100)):
    theta0, theta1 = parameters.theta0, parameters.theta1
    price_pred = theta0 + theta1 * mileage_range
    return mileage_range, price_pred

def theorical_linear_regression(data):
    x, y = np.array(data["x_normalized"]), np.array(data["y_normalized"])
    mean_x, mean_y = np.mean(x), np.mean(y)
    
    covariance = np.cov(x, y, bias=True)[0, 1]
    variance_x = np.var(x)
    
    normalized_theta1 = covariance / variance_x
    normalized_theta0 = mean_y - normalized_theta1 * mean_x
    
    theta0, theta1 = denormalize_parameters(normalized_theta0, normalized_theta1, data)
    return linear_regression(type('', (object,), {'theta0': theta0, 'theta1': theta1})())

def plot_results(algorithm_line, theoretical_line, data, loss,ax1,ax2):
    mileage_data, price_data = data["km"], data["price"]
    
    ax1.clear()
    ax2.clear()
    for line, style, label in zip([algorithm_line, theoretical_line], ['b-', 'g--'], ['Algorithm', 'Theoretical']):
        ax1.plot(*line, style, label=label)
    ax1.scatter(mileage_data, price_data, c='r', marker='o', label='Data points')
    
    ax1.set(xlim=(0, 250000), ylim=(0, 9000), xlabel='Mileage', ylabel='Price', title='Price Prediction Based on Mileage')
    ax1.grid(True)
    ax1.legend()
    
    if len(loss) != 0:
        if len(loss) < 100:
            loss = np.pad(loss, (0, 100 - len(loss) + 1), mode='edge')
        else:
            loss = np.array(loss)
        ax2.plot(loss, 'b-', label='Loss')
        ax2.set(xlim=(0, 100), ylim=(loss.min() * 0.9, loss.max() * 1.1), xlabel='Iterations', ylabel='Loss', title='Loss Function')
        ax2.legend()
    ax2.grid(True)

    plt.draw()
    plt.pause(0.01)

def update_plot(data, theorical_regression, parameters,ax1,ax2):
    parameters = load_parameters_from_json()
    ml_regression = linear_regression(parameters)

    plot_results(ml_regression, theorical_regression, data, parameters.loss,ax1,ax2)
    return ml_regression, parameters