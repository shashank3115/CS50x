#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    FILE *card = fopen(argv[1], "r");

    uint8_t buffer[512];

    int img_found = 0;
    int counter = 0;
    char filename[8];
    FILE *img = NULL;

    while (fread(buffer, 1, 512, card))
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xe0) == 0xe0)
        {
            img_found = 1;
        }
        if (img_found == 1)
        {
            if (counter != 0)
            {
                fclose(img);
            }
            sprintf(filename, "%03i.jpg", counter);
            img = fopen(filename, "a");
            fwrite(buffer, 1, 512, img);
            img_found = 0;
            counter += 1;
        }
        else if (counter != 0)
        {
            fwrite(buffer, 1, 512, img);
        }
    }
    fclose(img);
    fclose(card);
}
