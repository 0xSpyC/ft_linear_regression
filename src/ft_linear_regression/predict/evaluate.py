import sys
import threading
from ..utils.data_utils import load_parameters_from_json

def input_output_loop():
    while True:
        try:
            user_input = input("Enter a mileage: ")
            number = float(user_input)
            max_value = 100000000
            if number > max_value:
                print(f"Error: The mileage is too high.")
                continue
            elif number < 0: 
                print("Error: The mileage can't be negative")
                continue
            parameters = load_parameters_from_json()
            price = parameters.theta1 * number + parameters.theta0
            print(f"Price for {user_input} miles = {int(price)} $\n")
        except ValueError:
            print("Invalid input! Please enter an integer.", file=sys.stderr)

def read_input():
    input_thread = threading.Thread(target=input_output_loop, daemon=True)
    input_thread.start()