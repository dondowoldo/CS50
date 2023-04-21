from cs50 import get_float

# Prompt user for an amount in dollars an save into variable in form of cents


def main():
    while True:
        change = get_float("Change owed: ") * 100
        if change >= 0:
            break

    # Calls function that returns an integer to account for whole cents only
    # and subtract the amount from the total for a new total which is then passed into another functions

    quarters = calculate_quarters(change)
    change = change - quarters * 25

    dimes = calculate_dimes(change)
    change = change - dimes * 10

    nickels = calculate_nickels(change)
    change = change - nickels * 5

    pennies = calculate_pennies(change)
    change = change - pennies

    # Prints the total amount of coins returned to the customer

    sum = quarters + dimes + nickels + pennies
    print(sum)


# Calculate the number of quarters to give the customer

def calculate_quarters(change):
    quarters = change / 25
    return int(quarters)

# Calculate the number of dimes to give the customer


def calculate_dimes(change):
    dimes = change / 10
    return int(dimes)

# Calculate the number of nickels to give the customer


def calculate_nickels(change):
    nickels = change / 5
    return int(nickels)

# Calculate the number of pennies to give the customer


def calculate_pennies(change):
    pennies = change / 1
    return int(pennies)


if __name__ == "__main__":
    main()