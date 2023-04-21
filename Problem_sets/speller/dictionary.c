// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include "dictionary.h"
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Choose number of buckets in hash table
// (Until 1500 the performance increase was noticable but after 1500 I got very little performance increase
// for lots more allocated buckets across different texts)
const unsigned int N = 1500;

// Hash table
node *table[N];

// Word counter in dictionary
int word_counter = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    for (node *tmp = table[hash(word)]; tmp != NULL; tmp = tmp->next)
    {
        if (strcasecmp(tmp->word, word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Adds an ASCII value of each character in word, converts char into uppercase
    // to prevent having multiple buckets for same word with different casing
    // and returns added value divided with remainder of N to prevent seg fault.

    int added_values = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        added_values += toupper(word[i]);
    }
    added_values %= N;

    return added_values;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    char word[LENGTH + 1];
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    while (fscanf(file, "%s", word) != EOF)
    {
        node *w = malloc(sizeof(node));
        if (w == NULL)
        {
            free(w);
            return false;
        }

        strcpy(w->word, word);
        word_counter += 1;
        w->next = NULL;

        if (table[hash(w->word)] == NULL)
        {
            table[hash(w->word)] = w;
        }
        else
        {
            w->next = table[hash(word)];
            table[hash(w->word)] = w;
        }
    }

    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    int nullcounter = 0;
    node *tmp;

    for (int i = 0; i < N; i++)
    {
        while (table[i] != NULL)
        {
            tmp = table[i]->next;
            free(table[i]);
            table[i] = tmp;
        }
    }

    for (int i = 0; i < N; i++)
    {
        if (table[i] == NULL)
        {
            nullcounter += 1;
        }
    }

    if (nullcounter == N)
    {
        return true;
    }
    else
    {
        return false;
    }
}