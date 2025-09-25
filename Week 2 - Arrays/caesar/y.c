#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <cs50.h>
#include <stdlib.h>

int main(void)
{
    string text = get_string("plaintext:  ");
    for(int i = 0 , l = strlen(text) ; i < l ; i++)
    {
        if(isupper(text[i]))
        {
            char c = text[i] - 'A';
            char cipher = ((int) c + 2) % 26;
            char d = cipher + 'A';
            printf("%c",d);
        }
        else if(islower(text[i]))
        {
            char c = text[i] - 'a';
            char cipher = ((int) c + 2) % 26;
            char d = cipher + 'a';
            printf("%c",d);
        }
    }
    printf("\n");


}
