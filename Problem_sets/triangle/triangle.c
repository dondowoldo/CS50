
#include <stdio.h>
#include <cs50.h>

bool is_triangle(int x, int y, int z);


int main(void)
{
int x = get_int ("Enter the first lenght: \n");
int y = get_int ("Enter the second lenght: \n");
int z = get_int ("Enter the last lenght: \n");

    if (is_triangle(x, y, z) == true)
    {
        printf("This is a valid triangle\n");
    }
    else
    {
        printf("This is NOT a valid triangle\n");
    }

}




bool is_triangle(int x, int y, int z)
{

    if (x <= 0 || y <= 0 || z <= 0 )
    {
        return false;
    }
    else if ((x + y > z && x + z > y && y + z > x ))
    {
        return true;
    }
    else
    {
        return false;
    }
}