#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Enter text : ");
    float letters = count_letters(text);
    printf("%f\n", letters);
    float words = count_words(text);
    printf("%f\n", words);
    float sentences = count_sentences(text);
    printf("%f\n", sentences);

    // coleman-Lian index
    float L = letters / words * 100;
    float S = sentences / words * 100;

    float index = 0.0588 * L - 0.296 * S - 15.8;
    index = (int) round(index);

    // print grade level
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %d\n", (int) index);
    }
}

int count_letters(string text)
{
    int count = 0;
    for (int i = 0, len = strlen(text); i <= len; i++)
    {
        if (isupper(text[i]))
        {
            count = count + 1;
        }
        else if (islower(text[i]))
        {
            count = count + 1;
        }
    }
    return count;
}

int count_words(string text)
{
    int count = 1;
    for (int i = 0, len = strlen(text); i <= len; i++)
    {
        if (isblank(text[i]))
        {
            count = count + 1;
        }
    }
    return count;
}

int count_sentences(string text)
{
    int count = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
        if (text[i] == '.')
        {
            count += 1;
        }
        else if (text[i] == '?')
        {
            count += 1;
        }
        else if (text[i] == '!')
        {
            count += 1;
        }

    return count;
}
