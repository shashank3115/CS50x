#include <cs50.h>
#include <stdio.h>
#include <string.h>

typedef struct
{
    string name;
    int votes;
} candidate;

candidate new[3];
candidate candidates[3];
int main(void)
{
    candidates[0].name = "john";
    candidates[0].votes = 1;

    candidates[1].name = "shashank";
    candidates[1].votes = 0;

    candidates[2].name = "hello";
    candidates[2].votes = 3;


int maxvotes = 0;

for(int i = 0 ; i < 3 ; i++)
{
    if(candidates[i].votes > maxvotes)
    {
        maxvotes = candidates[i].votes;
    }
}

for(int i = 0 ; i < 3; i++)
{
    if(candidates[i].votes == maxvotes)
    {
        printf("%s\n",candidates[i].name);
    }
}

}


