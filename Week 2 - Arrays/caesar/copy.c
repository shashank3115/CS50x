#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <cs50.h>
#include <stdlib.h>

char rotate(char character , int key);



int main(int argc,string argv[])
{

    if(argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    string k = argv[1];
    int my_digit = atoi(k);

    for(int i = 0 , len = strlen(argv[1]) ; i < len ; i++)
    {
        if(!isdigit(argv[1][i]))
        {
         printf("Usage: ./caesar key\n");
         return 1;
        }
    }


        string text = get_string("Plaintext:  ");
        printf("ciphertext: ");

        for(int i = 0 , len = strlen(text) ; i <= len ; i++)
        {
            char my_character = text[i];
            char ciphertext = rotate(my_character,my_digit);
        }
        printf("\n");
        return 0;
}








char rotate(char character , int key)
{

        if(isalpha(character))
        {
            if(isupper(character))
            {
                char c =  character - 'A';
                char cipher = (c + key) % 26;
                char d = cipher + 'A';
                return d;
            }
            else if(islower(character))
            {
                char c = character - 'a';
                char cipher = (c + key) % 26;
                char e = cipher + 'a';
                return e;
            }
        }
        return character;
}

