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

# Example usage
card_number = input("Enter the credit card number: ")
if is_valid_credit_card(card_number):
    print("The credit card number is valid.")
else:
    print("The credit card number is fake or invalid.")