#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

bool only_unique_letters(string key);
void substitute(string text, string key);

// Checks if user inputs exactly one argument, and if not, program prints error message and quits.
int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("You must enter precisely 1 argument (cipher) that contains 26 alphabetical UNIQUE characters.\n");
        return 1;
    }

// Checks if user inputs a key containing letters only. Letters must be unique and cannot repeat.
    else if (only_unique_letters(argv[1]) == false)
    {
        printf("You must enter precisely 1 argument (cipher) that contains 26 alphabetical UNIQUE characters.\n");
        return 1;
    }

//  Prompts user for a text to be ciphered and then calls a function substitute that will convert the text
    string plaintext = get_string("plaintext: ");
    substitute(plaintext, argv[1]);
}

void substitute(string text, string key)
{
    int conversion_index = 0;
    printf("ciphertext: ");

// Looping m times where m is the lenght of a string that the user inputs (plaintext)
// Checking each character to confirm if it's a letter, and if not, prints that character unchanged as is.
// Then program checks if a letter is uppercase or lowercase and based on that subtracts the propriate ASCII value to get an alphabetical index.
// After that the original character is replaced by the character from the key with the same index.
// Casing stays intact due to functions toupper and tolower where appropriate.
    for (int j = 0, m = strlen(text); j < m; j++)
    {
        if (isalpha(text[j]) != 0)
        {
            if (isupper(text[j]) != 0)
            {
                conversion_index = text[j] - 65;
                text[j] = key[conversion_index];
                printf("%c", toupper(text[j]));
            }
            else
            {
                conversion_index = text[j] - 97;
                text[j] = key[conversion_index];
                printf("%c", tolower(text[j]));
            }

        }
        else
        {
            printf("%c", text[j]);
        }

    }
    printf("\n");
}

// 3 in 1 function that checks if the key contains exactly 26 characters
// if it doesn't, returns a false value. If it does, the function checks if all characters entered are alphabetical characters.
// Last part of the function checks for repetition.
// Inner loop always starts from 0 but checking the char just added so every new character that is added, the function checks all the previous letters.
// If repetition is recognised, function breaks the loop and returns false. If all conditions are met, returns true.
bool only_unique_letters(string key)
{
    char repeat_check[26];
    bool letters = false;
    int repeated = 0;

    if (strlen(key) == 26)
    {
        for (int i = 0, n = strlen(key); i < n; i++)
        {
            if (isalpha(key[i]) != 0)
            {
                letters = true;
                repeat_check[i] = tolower(key[i]);

                for (int j = 0, m = i; j < m; j++)
                {
                    if (repeat_check[j] == tolower(key[i]))
                    {
                        repeated = 1;
                        break;
                    }
                }
            }
            else
            {
                letters = false;
                break;
            }

            if (repeated == 1)
            {
                letters = false;
                break;
            }
        }
    }
    else
    {
        letters = false;
    }
    return letters;
}