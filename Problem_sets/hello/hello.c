#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //prompts a user to enter his name and stores this user input into variable "name"
    string name = get_string("What's your name?\n");
    // prints out "hello, "followed by a string value stored inside a variable "name"
    printf("Hello, %s\n", name);
}