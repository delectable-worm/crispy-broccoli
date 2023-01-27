import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Wrong usage!")
        exit(1)

    # TODO: Read database file into a variable
    database = []
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            database.append(row)
        # Get  string names
        strings = reader.fieldnames


    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2]) as file:
        sequence = file.read()



    # TODO: Find longest match of each STR in DNA sequence
    strmatch = {}
    #should be dict, not list
    for i in strings[1:]:
        strmatch[i] = str(longest_match(sequence, i))


    for person in database:
        count = 0
        for string in strings[1:]:
            if person[string] == strmatch[string]:
                #person string count included already
                count += 1
        if count == len(strmatch):
            print(person['name'])
            exit(0)
    print("No match")
    exit(0)

    # TODO: Check database for matching profiles
    #for i in strmatch:
     #   for j in database:



    return


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
