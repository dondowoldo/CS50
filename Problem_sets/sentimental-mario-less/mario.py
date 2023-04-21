import cs50

# Saves an int input by user into variable height that sets total height of the pyramid
while True:
    height = cs50.get_int("Height: ")
    if height > 0 and height < 9:
        break

# Firstly print spaces on each row equal to height-1 as with every hash printed on new line, amount of spaces is reduced by one.
# Then prints the amount of hashes equal to i+1 because we start with 1 hash, not zero
for i in range(height):
    for space in range(height-1):
        print(" ", end="")

    height -= 1
    for hash in range(i+1):
        print("#", end="")
    print()
