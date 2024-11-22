
num1 = int(input("Enter any number"))
num2 = int(input("Enter any number"))
try:
    divide = num1/num2
except Exception as e:
    print(f"Exception occured: {e}")
