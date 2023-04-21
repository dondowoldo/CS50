#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

// Checks if string passed into the function contains any other characters than digits. If so, returns false.
bool only_digits(string input);
char rotate(char c, int m);

// If more than 1 parameter is stated upon running the program, quits the program and tells user the correct usage.
// Secondly checks if parameter consists of digits only and if not, quits the program and tells user the correct usage.
int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else if (only_digits(argv[1]) == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

// Collecting input from the user and creating new int array with elements equal to the number of characters in user input.
    string plaintext = get_string("plaintext:  ");
    int input_array[strlen(plaintext)];

    printf("ciphertext: ");

// Looping through each character, calling rotate function and storing its rotated value inside of the int array to print out.
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        input_array[i] = rotate(plaintext[i], atoi(argv[1]));
        printf("%c", input_array[i]);
    }
    printf("\n");
    return 0;
}

// Rotates the characters by m amount. If letter is uppercase, lowercase or any other character.
// Subtracting according value of the first ASCII character independently (65 for upper case / 97 for lowercase) to convert into alphabetical order
// after recalculation adds back the subtracted value to convert back into ASCII.
char rotate(char c, int m)
{
    char rotated = '0';
    if (isupper(c) != 0)
    {
        rotated = c - 65;
        rotated = (rotated + m) % 26;
        rotated = rotated + 65;
    }
    else if (islower(c) != 0)
    {
        rotated = c - 97;
        rotated = (rotated + m) % 26;
        rotated = rotated + 97;
    }
    else if (isalpha(c) == 0)
    {
        rotated = c;
    }
    return rotated;

}
// Checks if string contains any other characters than digits.
// looping n times (lenght of the string) and as soon as finds a non-digit character, loop breaks and function returns false
// 
bool only_digits(string input)
{
    int digit = 0;

    for (int i = 0, n = strlen(input); i < n; i++)
    {
        if (isdigit(input[i]) == 0)
        {
            digit = 0;
            break;
        }
        else
        {
            digit = 1;
        }
    }
    if (digit == 0)
    {
        return false;
    }
    else
    {
        return true;
    }
}




