#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Enter the height: ");
    }
    while
    (n < 1 || n > 8);

    for (int i = 0; i < n; i++)
    {
        for (int k = 0; k < (n - 1 - i); k++)   // prints space each time it's necessary to Right-align the triangle correctly
        {
            printf(" ");
        }
        printf("#");                            // prints "#" in a loop until var i == height input by user


        for (int j = 0; j < i; j++)     // writes an additional "#" on the same row with each NEXT cycle until equal to var i
        {
            printf("#");
        }

        printf("  ");                   // prints out space between pyramids

        for (int l = 0; l <= i; l++)    // compare amount of "#" written in the left part and print if less or same amount
        {
            printf("#");
        }
        printf("\n");                   // after finishing 1 cycle we move onto the next row
    }



}