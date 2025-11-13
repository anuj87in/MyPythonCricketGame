def find_greater_math(a, b):
    """
    Find greater number using mathematical operations.
    Formula: max = (a + b + |a - b|) / 2
    
    Logic: If a > b, then |a - b| = a - b
           So, (a + b + a - b) / 2 = 2a / 2 = a
           If b > a, then |a - b| = b - a
           So, (a + b + b - a) / 2 = 2b / 2 = b
    """
    return (a + b + abs(a - b)) // 2


def find_greater_bitwise(a, b):
    """
    Find greater number using bit manipulation.
    Uses the sign bit of (a - b) to determine which is greater.
    """
    diff = a - b
    # Get sign bit: if diff >= 0, sign = 0; if diff < 0, sign = 1
    # For negative numbers in Python, we need special handling
    sign = (diff >> 31) & 1 if diff < 0 else 0
    
    # If sign = 0 (a >= b), return a
    # If sign = 1 (a < b), return b
    return a * (1 - sign) + b * sign


def find_greater_arithmetic(a, b):
    """
    Find greater number using pure arithmetic.
    Normalizes the difference to 0 or 1 and uses it as a selector.
    """
    diff = a - b
    # Normalize: if diff > 0, k = 1; if diff <= 0, k = 0
    k = int(bool(diff + abs(diff)))
    print(f"k is : {k}")
    
    
    return a * k + b * (1 - k)


# Main program with user input
if __name__ == "__main__":
    print("Finding Greater of Two Numbers (No Comparison Operators)")
    print("=" * 60)
    
    # Get user input
    try:
        a = int(input("\nEnter first number (a): "))
        b = int(input("Enter second number (b): "))
        
        print(f"\n{'=' * 60}")
        print(f"Numbers entered: {a} and {b}")
        print(f"{'=' * 60}")
        
        # Display results from all methods
        print(f"\nMethod 1 (Mathematical):  {find_greater_math(a, b)}")
        print(f"Method 2 (Bitwise):       {find_greater_bitwise(a, b)}")
        print(f"Method 3 (Arithmetic):    {find_greater_arithmetic(a, b)}")
        
        print(f"\nThe greater number is: {find_greater_math(a, b)}")
        
    except ValueError:
        print("\nError: Please enter valid integer numbers!")