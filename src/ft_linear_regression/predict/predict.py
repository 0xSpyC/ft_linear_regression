from ..utils.data_utils import load_parameters_from_json, load_normalized_data
from .plot import linear_regression, plot_results, theorical_linear_regression, update_plot
from .watchdog_handler import setup_watchdog_handler
import numpy as np
from .config import *
import matplotlib.pyplot as plt
import time

def main():

    parameters = load_parameters_from_json()
    data = load_normalized_data()
    
    ml_regression = linear_regression(parameters)
    theorical_regression = theorical_linear_regression(data)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))
    plt.ion()

    observer, event_loop = setup_watchdog_handler(data, theorical_regression, parameters, ax1, ax2)
    update_plot(data, theorical_regression, parameters, ax1, ax2)

    try:
        event_loop()
    except KeyboardInterrupt:
        print("Stopping the program...")
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()