import tkinter as tk
from tkinter import messagebox, ttk
from sympy import symbols, diff, sympify, SympifyError

# Predefined exercises
EXERCISES = {
    "Exercise 1": {"function": "x**2 + 3*x + 2", "variable": "x"},
    "Exercise 2": {"function": "sin(x) + cos(x)", "variable": "x"},
    "Exercise 3": {"function": "exp(x) + log(x)", "variable": "x"},
    "Exercise 4": {"function": "x**3 - 2*x**2 + x - 5", "variable": "x"},
    "Exercise 5": {"function": "tan(x)", "variable": "x"},
}

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

def load_exercise(event):
    # Get the selected exercise
    selected_exercise = exercise_combobox.get()
    
    if selected_exercise in EXERCISES:
        # Load the function and variable into the input fields
        entry_function.delete(0, tk.END)
        entry_function.insert(0, EXERCISES[selected_exercise]["function"])
        
        entry_variable.delete(0, tk.END)
        entry_variable.insert(0, EXERCISES[selected_exercise]["variable"])

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

# Dropdown for predefined exercises
exercise_label = tk.Label(root, text="Select a predefined exercise:")
exercise_label.pack(pady=10)

exercise_combobox = ttk.Combobox(root, values=list(EXERCISES.keys()), state="readonly")
exercise_combobox.pack(pady=10)
exercise_combobox.bind("<<ComboboxSelected>>", load_exercise)

compute_button = tk.Button(root, text="Compute Derivative", command=compute_derivative)
compute_button.pack(pady=20)

result_label = tk.Label(root, text="Derivative: ")
result_label.pack(pady=10)

# Run the application
root.mainloop()