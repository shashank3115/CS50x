#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <cs50.h>
#include <stdlib.h>

char rotate(char q , int key);

int main(void)
{

    string text = get_string("plaintext:  ");
    int key = 2;
    printf("ciphertext: ");

    for(int i = 0 , len = strlen(text) ; i <= len ; i++)
    {
        char q = text[i];
        char ciphertext = rotate(q,key);
        printf("%c",ciphertext);
    }
    printf("\n");
}




char rotate(char character , int key)
{

        if(isalpha(character))
        {
                if(isupper(character))
            {
                char c =  character - 'A';
                char cipher = ((int) c + key) % 26;
                char d = cipher + 'A';
                return d;
            }
            else if(islower(q))
            {
                char c = character - 'a';
                char cipher = ((int) c + key) % 26;
                char e = cipher + 'a';
                return e;
            }
        }
        else
        {
            return character;
        }
        return 0;
}

