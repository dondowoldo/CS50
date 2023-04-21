#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int tempavg = 0;
    for (int i = 0, n = height; i < n; i++) // Looping while taking average of rgb in one pixel and setting it to the same value.
    {
        for (int j = 0, m = width; j < m; j++)
        {
            tempavg = round(((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0));

            image[i][j].rgbtBlue = tempavg;
            image[i][j].rgbtGreen = tempavg;
            image[i][j].rgbtRed = tempavg;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE mirrored[height][width];

    for (int i = 0, n = height; i < n; i++) // First loop copying reverted pixels into mirrored array.
    {
        int mirroredwidth = width - 1;

        for (int j = 0, m = width; j < m; j++)
        {
            mirrored[i][j].rgbtBlue = image[i][mirroredwidth].rgbtBlue;
            mirrored[i][j].rgbtGreen = image[i][mirroredwidth].rgbtGreen;
            mirrored[i][j].rgbtRed = image[i][mirroredwidth].rgbtRed;
            mirroredwidth = mirroredwidth - 1;
        }
    }

    for (int k = 0, o = height; k < o; k++) // Second loop puting reverted pixels back into origianl image.
    {
        for (int l = 0, p = width; l < p; l++)
        {
            image[k][l].rgbtBlue = mirrored[k][l].rgbtBlue;
            image[k][l].rgbtGreen = mirrored[k][l].rgbtGreen;
            image[k][l].rgbtRed = mirrored[k][l].rgbtRed;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int avgBlue = 0;
    int avgGreen = 0;
    int avgRed = 0;
    RGBTRIPLE blurred[height][width];

// 4 corner pixels done first, then all sides right on the edge, and then the rest

    for (int i = 0, n = height; i < n; i++)
    {
        for (int j = 0, k = width; j < k; j++)
        {
            if (i == 0 && j == 0)   // top left corner
            {
                avgBlue = round((image[0][0].rgbtBlue + image[0][1].rgbtBlue + image[1][0].rgbtBlue + image[1][1].rgbtBlue) / 4.0);
                avgGreen = round((image[0][0].rgbtGreen + image[0][1].rgbtGreen + image[1][0].rgbtGreen + image[1][1].rgbtGreen) / 4.0);
                avgRed = round((image[0][0].rgbtRed + image[0][1].rgbtRed + image[1][0].rgbtRed + image[1][1].rgbtRed) / 4.0);
                blurred[0][0].rgbtBlue = avgBlue;
                blurred[0][0].rgbtGreen = avgGreen;
                blurred[0][0].rgbtRed = avgRed;
            }
            else if (i == height - 1 && j == 0) // bottom left corner
            {
                avgBlue = round((image[height - 1][0].rgbtBlue + image[height - 1][1].rgbtBlue + image[height - 2][0].rgbtBlue +
                                 image[height - 2][1].rgbtBlue) / 4.0);
                avgGreen = round((image[height - 1][0].rgbtGreen + image[height - 1][1].rgbtGreen + image[height - 2][0].rgbtGreen +
                                  image[height - 2][1].rgbtGreen) / 4.0);
                avgRed = round((image[height - 1][0].rgbtRed + image[height - 1][1].rgbtRed + image[height - 2][0].rgbtRed +
                                image[height - 2][1].rgbtRed) / 4.0);
                blurred[height - 1][0].rgbtBlue = avgBlue;
                blurred[height - 1][0].rgbtGreen = avgGreen;
                blurred[height - 1][0].rgbtRed = avgRed;
            }
            else if (i == 0 && j == width - 1)  // top right corner
            {
                avgBlue = round((image[0][width - 1].rgbtBlue + image[0][width - 2].rgbtBlue + image[1][width - 1].rgbtBlue +
                                 image[1][width - 2].rgbtBlue) / 4.0);
                avgGreen = round((image[0][width - 1].rgbtGreen + image[0][width - 2].rgbtGreen + image[1][width - 1].rgbtGreen +
                                  image[1][width - 2].rgbtGreen) / 4.0);
                avgRed = round((image[0][width - 1].rgbtRed + image[0][width - 2].rgbtRed + image[1][width - 1].rgbtRed +
                                image[1][width - 2].rgbtRed) / 4.0);
                blurred[0][width - 1].rgbtBlue = avgBlue;
                blurred[0][width - 1].rgbtGreen = avgGreen;
                blurred[0][width - 1].rgbtRed = avgRed;
            }
            else if (i == height - 1 && j == width - 1) // bottom right corner
            {
                avgBlue = round((image[height - 1][width - 1].rgbtBlue + image[height - 1][width - 2].rgbtBlue +
                                 image[height - 2][width - 1].rgbtBlue + image[height - 2][width - 2].rgbtBlue) / 4.0);
                avgGreen = round((image[height - 1][width - 1].rgbtGreen + image[height - 1][width - 2].rgbtGreen +
                                  image[height - 2][width - 1].rgbtGreen + image[height - 2][width - 2].rgbtGreen) / 4.0);
                avgRed = round((image[height - 1][width - 1].rgbtRed + image[height - 1][width - 2].rgbtRed +
                                image[height - 2][width - 1].rgbtRed + image[height - 2][width - 2].rgbtRed) / 4.0);
                blurred[height - 1][width - 1].rgbtBlue = avgBlue;
                blurred[height - 1][width - 1].rgbtGreen = avgGreen;
                blurred[height - 1][width - 1].rgbtRed = avgRed;
            }
            else if ((i >= 1 && j == 0) && (i <= height - 2 && j == 0)) // left side
            {
                avgBlue = round((image[i][j].rgbtBlue + image[i - 1][j].rgbtBlue + image[i + 1][j].rgbtBlue + image[i - 1][j + 1].rgbtBlue +
                                 image[i][j + 1].rgbtBlue + image[i + 1][j + 1].rgbtBlue) / 6.0);
                avgGreen = round((image[i][j].rgbtGreen + image[i - 1][j].rgbtGreen + image[i + 1][j].rgbtGreen + image[i - 1][j + 1].rgbtGreen +
                                  image[i][j + 1].rgbtGreen + image[i + 1][j + 1].rgbtGreen) / 6.0);
                avgRed = round((image[i][j].rgbtRed + image[i - 1][j].rgbtRed + image[i + 1][j].rgbtRed + image[i - 1][j + 1].rgbtRed +
                                image[i][j + 1].rgbtRed + image[i + 1][j + 1].rgbtRed) / 6.0);
                blurred[i][j].rgbtBlue = avgBlue;
                blurred[i][j].rgbtGreen = avgGreen;
                blurred[i][j].rgbtRed = avgRed;
            }
            else if ((i == height - 1 && j >= 1) && (i == height - 1 && j <= width - 2))    // bottom side)
            {
                avgBlue = round((image[i][j].rgbtBlue + image[i][j - 1].rgbtBlue + image[i][j + 1].rgbtBlue + image[i - 1][j - 1].rgbtBlue +
                                 image[i - 1][j].rgbtBlue + image[i - 1][j + 1].rgbtBlue) / 6.0);
                avgGreen = round((image[i][j].rgbtGreen + image[i][j - 1].rgbtGreen + image[i][j + 1].rgbtGreen + image[i - 1][j - 1].rgbtGreen +
                                  image[i - 1][j].rgbtGreen + image[i - 1][j + 1].rgbtGreen) / 6.0);
                avgRed = round((image[i][j].rgbtRed + image[i][j - 1].rgbtRed + image[i][j + 1].rgbtRed + image[i - 1][j - 1].rgbtRed +
                                image[i - 1][j].rgbtRed + image[i - 1][j + 1].rgbtRed) / 6.0);
                blurred[i][j].rgbtBlue = avgBlue;
                blurred[i][j].rgbtGreen = avgGreen;
                blurred[i][j].rgbtRed = avgRed;
            }
            else if ((i >= 1 && j == width - 1) && (i <= height - 2 && j == width - 1))    // right side)
            {
                avgBlue = round((image[i][j].rgbtBlue + image[i - 1][j].rgbtBlue + image[i + 1][j].rgbtBlue + image[i - 1][j - 1].rgbtBlue +
                                 image[i][j - 1].rgbtBlue + image[i + 1][j - 1].rgbtBlue) / 6.0);
                avgGreen = round((image[i][j].rgbtGreen + image[i - 1][j].rgbtGreen + image[i + 1][j].rgbtGreen + image[i - 1][j - 1].rgbtGreen +
                                  image[i][j - 1].rgbtGreen + image[i + 1][j - 1].rgbtGreen) / 6.0);
                avgRed = round((image[i][j].rgbtRed + image[i - 1][j].rgbtRed + image[i + 1][j].rgbtRed + image[i - 1][j - 1].rgbtRed +
                                image[i][j - 1].rgbtRed + image[i + 1][j - 1].rgbtRed) / 6.0);
                blurred[i][j].rgbtBlue = avgBlue;
                blurred[i][j].rgbtGreen = avgGreen;
                blurred[i][j].rgbtRed = avgRed;
            }
            else if ((i == 0 && j >= 1) && (i == 0 && j <= width - 2))  // top side
            {
                avgBlue = round((image[i][j].rgbtBlue + image[i][j - 1].rgbtBlue + image[i][j + 1].rgbtBlue + image[i + 1][j - 1].rgbtBlue +
                                 image[i + 1][j].rgbtBlue + image[i + 1][j + 1].rgbtBlue) / 6.0);
                avgGreen = round((image[i][j].rgbtGreen + image[i][j - 1].rgbtGreen + image[i][j + 1].rgbtGreen + image[i + 1][j - 1].rgbtGreen +
                                  image[i + 1][j].rgbtGreen + image[i + 1][j + 1].rgbtGreen) / 6.0);
                avgRed = round((image[i][j].rgbtRed + image[i][j - 1].rgbtRed + image[i][j + 1].rgbtRed + image[i + 1][j - 1].rgbtRed +
                                image[i + 1][j].rgbtRed + image[i + 1][j + 1].rgbtRed) / 6.0);
                blurred[i][j].rgbtBlue = avgBlue;
                blurred[i][j].rgbtGreen = avgGreen;
                blurred[i][j].rgbtRed = avgRed;
            }
            else    // rest of the image
            {
                avgBlue = round((image[i][j].rgbtBlue + image[i][j - 1].rgbtBlue + image[i][j + 1].rgbtBlue +
                                 image[i - 1][j - 1].rgbtBlue + image[i - 1][j].rgbtBlue + image[i - 1][j + 1].rgbtBlue +
                                 image[i + 1][j - 1].rgbtBlue + image[i + 1][j].rgbtBlue + image[i + 1][j + 1].rgbtBlue) / 9.0);
                avgGreen = round((image[i][j].rgbtGreen + image[i][j - 1].rgbtGreen + image[i][j + 1].rgbtGreen +
                                  image[i - 1][j - 1].rgbtGreen + image[i - 1][j].rgbtGreen + image[i - 1][j + 1].rgbtGreen +
                                  image[i + 1][j - 1].rgbtGreen + image[i + 1][j].rgbtGreen + image[i + 1][j + 1].rgbtGreen) / 9.0);
                avgRed = round((image[i][j].rgbtRed + image[i][j - 1].rgbtRed + image[i][j + 1].rgbtRed + image[i - 1][j - 1].rgbtRed +
                                image[i - 1][j].rgbtRed + image[i - 1][j + 1].rgbtRed + image[i + 1][j - 1].rgbtRed +
                                image[i + 1][j].rgbtRed + image[i + 1][j + 1].rgbtRed) / 9.0);
                blurred[i][j].rgbtBlue = avgBlue;
                blurred[i][j].rgbtGreen = avgGreen;
                blurred[i][j].rgbtRed = avgRed;
            }
        }
    }

    for (int l = 0, o = height; l < o; l++) // final loop copying blurred pixels into original picture
    {
        for (int q = 0, p = width; q < p; q++)
        {
            image[l][q].rgbtBlue = blurred[l][q].rgbtBlue;
            image[l][q].rgbtGreen = blurred[l][q].rgbtGreen;
            image[l][q].rgbtRed = blurred[l][q].rgbtRed;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
