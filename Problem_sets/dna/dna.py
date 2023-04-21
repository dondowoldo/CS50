import csv
import sys


def main():

    # Read database file into a variable
    # Saves the keys (STRs) into a variable minus the first value (name)
    if len(sys.argv) != 3:
        sys.exit('Usage: "dna filename(csv) filename(text)"')
    else:
        database = []
        with open(sys.argv[1], "r") as csvfile:
            dictReader = csv.DictReader(csvfile)
            for person in dictReader:
                database.append(person)
        STRs = list(database[0].keys())[1:]

    # Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as sequencefile:
        sequence = sequencefile.read()

    # Find longest match of each STR in DNA sequence
    # Looping i times where i is the amount of STRs stored
    # Calling a function to get the maximum continual repetition of given STR and saves it into variable

        STRcount = {}
    for i in range(len(STRs)):
        STRcount[STRs[i]] = longest_match(sequence, STRs[i])

    # Check database for matching profiles
    # Looping through every name in outer loop and every STR in inner loop
    # For every correct match of given STR counter adds 1 and then compares to the total amount of STRs

    for i in range(len(database)):
        correct_counter = 0
        for j in range(len(STRs)):
            if int(database[i][STRs[j]]) == STRcount[STRs[j]]:
                correct_counter += 1

        if correct_counter == len(STRs):
            print(database[i]["name"])
            return

    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
