#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
char LETTERS[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};
int compute_score(string word);


int main(void)
{

    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Print results
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }

}
// Firstly checks how many characters are in a string.
// Saves a character into variable and checks if it is an uppercase char or any other non-letter char.
// If it's an uppercase char, it coverts it into a lowercase. If it's any other non-letter char, score for this char is "0"
// If char is valid char, loops keep checking until the char matches the value of char array and checks for the value
// of that element in the int array.
// Lastly the final score is then passed into a variable.

int compute_score(string word)
{
    int tempscore = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {

        char tempchar = word[i];
        int m = 0;

        if (isupper(tempchar) != 0)
        {
            tempchar = tolower(tempchar);
        }

        if ((tempchar < 65) || (tempchar > 90 && tempchar < 97) || (tempchar > 123))
        {
            int nullpoint = 0;
            tempscore = tempscore + nullpoint;
        }
        else
        {
            while (LETTERS[m] != tempchar)
            {
                m++;
            }
            tempscore = tempscore + POINTS[m];
        }

    }
    return tempscore;
}
