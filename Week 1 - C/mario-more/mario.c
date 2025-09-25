#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int rows;
    do
    {
        rows=get_int("Height: ");
    }
    while ((rows < 1 ) || (rows > 8));

    for(int i = 0 ; i < rows ; i++)
    {
        for(int j = 0 ; j < rows - 1 - i ; j++)
        {
            printf(" ");
        }
        for(int k = 0 ; k <= i ; k++)
        {
            printf("#");
        }
        printf("  ");

        for(int b = 0 ; b <= i ; b++)
        {
            printf("#");
        }
        printf("\n");

    }

}
