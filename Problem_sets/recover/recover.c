#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <cs50.h>

typedef uint8_t BYTE;
const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    if (argc != 2)  // Make sure user enters a name of the file
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");   // open the specified file
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    BYTE buffer[BLOCK_SIZE];    // create an array to store data in from the file
    char *filename;
    filename = malloc(8 * sizeof(BYTE));    // need 8 bytes for 8 characters total "000.jpg" + \0
    bool first_jpeg_found = false;
    FILE *output;
    int filecounter = 0; // accounts for every image written and determines new filename

    while (fread(buffer, sizeof(BYTE), BLOCK_SIZE, input) == BLOCK_SIZE) // repeat until end of file
    {
        // determine if possibly a jpeg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (first_jpeg_found == false)  // start writing data for the first jpg identified and keep writing until next jpg is identified.
            {
                sprintf(filename, "%03i.jpg", filecounter);
                output = fopen(filename, "w");
                if (output == NULL)
                {
                    printf("Could not open file.\n");
                    return 1;
                }

                filecounter = filecounter + 1;
                fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, output);
                first_jpeg_found = true;
            }
            else    // closes a file and opens a new one as soon as new jpg is identified
            {
                fclose(output);
                sprintf(filename, "%03i.jpg", filecounter);
                output = fopen(filename, "w");
                if (output == NULL)
                {
                    printf("Could not open file.\n");
                    return 1;
                }
                filecounter = filecounter + 1;
                fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, output);
            }
        }
        else if (first_jpeg_found == true)
        {
            fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, output);
        }
    }

    fclose(input);
    fclose(output);
    free(filename);
}