#include <cs50.h>
#include <stdio.h>

int main(void)
{
    bool acceptable = false;
    int input;
    while(!acceptable)
    {
        input = get_int("How many rows? ");
        if(input>0)
        {
            acceptable=true;
        }
    }
    for (int i=1; i<=input; i++) //starts at 1 for easier use of i
    {
        for (int j=0; j<(input-i); j++) //itial gap
        {
            printf(" ");
        }
        for (int j=0; j<i; j++) //hash 1
        {
            printf("#");
        }
        printf("  ");
        for (int j=0; j<i; j++) //hash 2 -- same as 1
        {
            printf("#");
        }
        printf("\n");
    }
}

