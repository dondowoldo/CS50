#include <stdio.h>
#include <stdlib.h>

typedef struct node
{
    int number;
    struct node *next;

}
node;

int main (void)
{

    node *list = malloc(sizeof(node));  // allocate a space in memory for node and make pointer "list" point to it -->
    if (list == NULL)
    {
        return 1;
    }

    list->number = 4;   // GO to the address that list is pointing at and set the .number parameter to "4"

    //////////////////////////////////////////////////////////////////////////////////////////////////////

    // Allocate a space in memory for another node, and make the pointer in the first node point to this one

    list->next = malloc(sizeof(node));
    if (list->next == NULL)
    {
        free(list->next);
        return 1;
    }

    list->next->number = 5;     // GO to the address that list is pointing to, and go to the address stored at next and change number value to "5"

    list->next->next = NULL;

    printf("first node number : %i\n", list->number); // OR =    (*list).number);   (Both expressions have the same meaning.)

    printf("second node number : %i\n", list->next->number);


    // LOOP TO PRINT NUMBERS IN LINKED NODES
    // 1.)Temporary variable that points to the same node as "list" does.
    // 2.) Keep looping as long as pointing at VALID node.
    // 3.) Go to the number in node that "tmp" is pointing at and print. Then change "tmp" to whatever is at "tmp" and grabbing the "next" field.

    for (node *tmp = list; tmp != NULL; tmp = tmp->next)
    {
        printf("looped print : %i\n", tmp->number);
    }


    // LOOP TO FREE MEMORY IN LINKED NODES (Loop continues until the list points at null)
    // 1.) Create temporary var that points at the second node
    // 2.) First node (list) is now OK to free as tmp links the rest
    // 3.) After the first node is freed, set list to be the same as temp (2nd node)

    while (list != NULL)
    {
        node *tmp = list->next;
        free(list);
        list = tmp;
    }
    return 0;
}