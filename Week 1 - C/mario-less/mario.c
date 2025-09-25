#include <cs50.h>
#include <stdio.h>

void print_row(int spaces, int bricks);
int main(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while ((n < 1) || (n > 8));

    for (int i = 0; i < n; i++)
    {
        print_row(n - 1 - i, i);
    }
}

void print_row(int spaces, int bricks)
{
    for (int j = 0; j < spaces; j++)
    {
        printf(" ");
    }
    for (int k = 0; k <= bricks; k++)
    {
        printf("#");
    }
    printf("\n");
}
