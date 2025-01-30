import tkinter as tk
from tkinter import messagebox

def is_valid_credit_card(card_number):
    # Remove any spaces or non-digit characters
    card_number = ''.join(filter(str.isdigit, card_number))
    
    # Check if the card number is empty or too short
    if not card_number or len(card_number) < 13 or len(card_number) > 19:
        return False
    
    # Convert the card number into a list of integers
    digits = [int(digit) for digit in card_number]
    
    # Double every second digit from the right
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] = digits[i] - 9
    
    # Sum all the digits
    total_sum = sum(digits)
    
    # Check if the sum is divisible by 10
    return total_sum % 10 == 0

def validate_card():
    card_number = entry.get()  # Get the card number from the input field
    if is_valid_credit_card(card_number):
        messagebox.showinfo("Result", "The credit card number is valid.")
    else:
        messagebox.showinfo("Result", "The credit card number is fake or invalid.")

# Create the main window
root = tk.Tk()
root.title("Credit Card Validator")

# Create a label and entry field for the card number
label = tk.Label(root, text="Enter Credit Card Number:")
label.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Create a button to trigger the validation
validate_button = tk.Button(root, text="Validate", command=validate_card)
validate_button.pack(pady=10)

# Run the application
root.mainloop()