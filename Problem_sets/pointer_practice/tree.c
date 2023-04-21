#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct node
{
    int number;
    struct node *left;
    struct node *right;
}
node;

void free_tree(node *root);
void print_tree(node *root);
bool search(node *root, int number);


int main (void)
{
    // Tree of size 0
    node *tree = NULL;

    // Add number to list
    node *n = malloc(sizeof(node));
    if (n == NULL)
    {
        return 1;
    }
    n->number = 2;
    n->left = NULL;
    n->right = NULL;
    tree = n;

    // Add number to list
    n = malloc(sizeof(node));
    if (n == NULL)
    {
        return 1;
    }
    n->number = 1;
    n->left = NULL;
    n->right = NULL;
    tree->left = n;

    // Add number to list
    n = malloc(sizeof(node));
    if (n == NULL)
    {
        return 1;
    }
    n->number = 3;
    n->left = NULL;
    n->right = NULL;
    tree->right = n;

    // Print tree
    print_tree(tree);


    // Binary search

    search(tree, 3);

    // checkup for successful search
    if (search(tree, 3) == true)
    {
        printf("Success\n");
    }
    else
    {
        printf("Number not found\n");
    }

    // Free tree
    free(tree);
}

void print_tree(node *root) // Prints lowest elements to highest recursively (can swap left/ right for reverse order)
{
    if (root == NULL)
    {
        return;
    }
    print_tree(root->left);
    printf("%i\n", root->number);
    print_tree(root->right);

}

void free_tree(node *root)
{
    if (root == NULL)
    {
        return;
    }
    free_tree(root->left);
    free_tree(root->right);
    free(root);
}

bool search(node *root, int number)
{
    if (root == NULL)
    {
        return false;
    }
    else if (number < root->number)
    {
        return search(root->left, number);
    }
    else if (number > root->number)
    {
        return search(root->right, number);
    }
    else
    {
        return true;
    }
}