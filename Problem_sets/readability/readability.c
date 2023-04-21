#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int count_letters(string text), count_words(string text), count_sentences(string text), coleman_index(int l, int w, int s);

int main(void)
{
    string text = get_string("Text: "); // Prompt a user for input text

// Prints Grade +16 if the rounded coleman index is greater or equal to 16
    if (coleman_index(count_letters(text), count_words(text), count_sentences(text)) >= 16)
    {
        printf("Grade 16+\n");
    }   // Prints Before Grade 1 if the rounded coleman index is less than 1
    else if (coleman_index(count_letters(text), count_words(text), count_sentences(text)) < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", coleman_index(count_letters(text), count_words(text), count_sentences(text)));
    }
}



// Checking for a string lenght n and looping n times counting letters.
int count_letters(string text)
{
    int letters = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]) != 0)  // checks if a character is an alphabetic value (a letter)
        {
            letters++;
        }
    }
    return letters;
}

// Checking for a string lenght n and looping n times counting words based on number of spaces used to divide words
int count_words(string text)
{
    int words, spaces = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == 32)
        {
            spaces++;
        }
    }
    words = spaces + 1;
    return words;
}

// Checking for a string lenght n and looping n times searching for '?' '!' '.' in ASCII values and returning that number as a number of sentences
int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == 46 || text[i] == 33 || text[i] == 63)
        {
            sentences++;
        }
    }
    return sentences;
}

// function calculating readability grading based on the Coleman-Liau index
int coleman_index(int l, int w, int s)
{
    float f = (l / (float)w) * 100;
    float g = (s / (float)w) * 100;
    float index = (0.0588 * f) - (0.296 * g) - 15.8;
    return round(index);
}