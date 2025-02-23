#  Sample Python Code for PR Review Bot Testing

def factorial(n):
    """Calculate factorial using recursion."""
    if n < 0:
        return "Error: Negative number not allowed."
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def is_prime(num):
    """Check if a number is prime."""
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

# Test Cases
print(factorial(5))  # Expected output: 120
print(is_prime(11))  # Expected output: True
