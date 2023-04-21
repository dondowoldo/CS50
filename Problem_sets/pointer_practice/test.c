#include <stdio.h>
#include <cs50.h>

void swap(int *a, int *b);

int main(void)
{
    int x = 50;
    int y = 20;

    printf("x is: %i, y is: %i\n", x, y);

    swap(&x, &y);

    printf("x is: %i, y is: %i\n", x, y);
}

void swap(int *a, int *b)
{
    int tmp = *a;
    *a = *b;
    *b = tmp;
}