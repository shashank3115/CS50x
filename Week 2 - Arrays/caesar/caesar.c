#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char rotate(char character, int key);

int main(int argc, string argv[])
{
    if (argc != 2) // Check if only one argument is passed (excluding program name)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    string key_str = argv[1];
    for (int i = 0, len = strlen(key_str); i < len; i++)
    {
        if (!isdigit(key_str[i])) // Check if the key is a digit
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    int key = atoi(key_str); // Convert the key to an integer

    string text = get_string("Plaintext: ");

    printf("Ciphertext: ");

    for (int i = 0, len = strlen(text); i < len; i++)
    {
        char my_character = text[i];
        char ciphertext = rotate(my_character, key);
        printf("%c", ciphertext);
    }

    printf("\n");
    return 0;
}

char rotate(char character, int key)
{
    if (isalpha(character))
    {
        if (isupper(character))
        {
            char c = character - 'A';
            char cipher = (c + key) % 26;
            char result = cipher + 'A';
            return result;
        }
        else if (islower(character))
        {
            char c = character - 'a';
            char cipher = (c + key) % 26;
            char result = cipher + 'a';
            return result;
        }
    }
    return character; // If not an alphabet, return the character unchanged
}
