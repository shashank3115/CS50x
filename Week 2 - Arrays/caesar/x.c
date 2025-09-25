#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <cs50.h>
#include <stdlib.h>

int main(int argc,string argv[])
{
    string k = argv[1];
    int digit = atoi(k);

    string text = get_string("plaintext:  ");


    for(int i = 0 , len = strlen(text) ; i <= len ; i++)
    {
        if(isalpha(text[i]))
        {
            char character = text[i] + digit;
            if(isupper(character))
            {
                char q = toupper(character);
                printf("%c",q);
            }
            else if(islower(character))
            {
                char r = tolower(character);
                printf("%c",r);
             }
        }
        else
        {
            printf("%c",text[i]);
        }

    }
    printf("\n");


}
