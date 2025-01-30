import tkinter as tk
from tkinter import messagebox
from sympy import symbols, diff, sympify, SympifyError


def compute_derivative():
    # Get the function and variable from the input fields
    function_input = entry_function.get()
    variable_input = entry_variable.get()

    try:
        # Define the symbol for the variable
        x = symbols(variable_input)
        
        # Convert the input function to a symbolic expression
        function = sympify(function_input)
        
        # Compute the derivative
        derivative = diff(function, x)
        
        # Display the result
        result_label.config(text=f"Derivative: {derivative}")
    except SympifyError:
        messagebox.showerror("Error", "Invalid function input. Please enter a valid mathematical function.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Derivative Solver")

# Create and place widgets
label_function = tk.Label(root, text="Enter the function (e.g., x**2 + 2*x + 1):")
label_function.pack(pady=10)

entry_function = tk.Entry(root, width=40)
entry_function.pack(pady=10)

label_variable = tk.Label(root, text="Enter the variable (e.g., x):")
label_variable.pack(pady=10)

entry_variable = tk.Entry(root, width=10)
entry_variable.pack(pady=10)

compute_button = tk.Button(root, text="Compute Derivative", command=compute_derivative)
compute_button.pack(pady=20)

result_label = tk.Label(root, text="Derivative: ")
result_label.pack(pady=10)

# Run the application
root.mainloop()