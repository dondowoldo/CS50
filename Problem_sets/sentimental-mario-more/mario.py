from cs50 import get_int

# Prompts user for a height
while True:
    height = get_int("Height: ")
    if height >= 1 and height <= 8:
        break

# Prints spaces to align the left pyramid and the first hash
for i in range(height):
    for n in range(height - 1 - i):
        print(" ", end="")
    print("#", end="")

    # Prints the rest of hashes for the first pyramid + double space
    for m in range(i):
        print("#", end="")
    print("  ", end="")

    # Prints the right pyramid
    for k in range(i + 1):
        print("#", end="")
    print()