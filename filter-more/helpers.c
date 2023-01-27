#include "helpers.h"
#include <math.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i<height; i++)
    {
        for(int j = 0; j<width; j++)
        {
            int average = round((image[i][j].rgbtGreen + image[i][j].rgbtRed + image[i][j].rgbtBlue)/3.0);

            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i<height; i++)
    {
        for (int j = 0; j<width/2; j++)
        {
            RGBTRIPLE store = image[i][width-1-j];
            image[i][width-1-j]=image[i][j];
            image[i][j]=store;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int red; int green; int blue;
    int blurAmount=1; double blurP=0;
    RGBTRIPLE copy[height][width];

    for (int i =0; i< height; i++) // make  copy
    {
        for (int j = 0; j<width; j++)
        {
            copy[i][j]=image[i][j];
        }
    }


    for (int i =0; i< height; i++)
    {
        for (int j = 0; j<width; j++)
        {
            blue=0; green=0; red=0; blurP=0;

            for(int k = i-blurAmount; k<=i+blurAmount; k++) // get average of surroundings
            {
                for(int l = j-blurAmount; l<=j+blurAmount; l++)
                {
                    if(k>=0 && k<height && l >= 0 && l<width)
                    {
                    red += copy[k][l].rgbtRed;
                    blue += copy[k][l].rgbtBlue;
                    green += copy[k][l].rgbtGreen;
                    blurP++;
                    }
                }
            }

            red = round(red / blurP);
            blue = round(blue/blurP);
            green = round(green/blurP);
            image[i][j].rgbtRed = red;
            image[i][j].rgbtGreen = green;
            image[i][j].rgbtBlue = blue;
        }
    }

    return;
}

/*
[i-1][j-1][i-1][j][1-1][j+1]


*/
// Detect edges
void mono(int height, int width, RGBTRIPLE image[height][width])
{
    int Xred; int Xgreen; int Xblue;
    int Yred; int Ygree; int Yblue;
    int red; int blue; int green;

    int Gx[3][3]=
    {
        {-1,0,1},
        {-2,0,2},
        {-1,0,1}
    };
    int Gy[3][3]=
    {
        {-1,-2,-1},
        {0,0,0},
        {1,2,1}
    };
    RGBTRIPLE copy[height][width];
    for (int i =0; i< height; i++) // make  copy // [columns][rows]
    {
        for (int j = 0; j<width; j++)
        {
            copy[i][j]=image[i][j];
        }
    }

    for (int i = 0; i<height; i++)
    {
        for (int j = 0; j<width; j++)
        {
            Xred=0;Xblue=0;Xgreen=0;
            Yred=0; Ygree=0; Yblue=0;
            for(int k=0;k<3; k++) // inner loop for getting 3x3 array
            {
                for(int l = 0; l<3; l++)
                {
                    Xred += copy[k-1+i][l-1+j].rgbtRed*Gx[k][l];
                    Xblue += copy[k-1+i][l-1+j].rgbtBlue*Gx[k][l];
                    Xgreen += copy[k-1+i][l-1+j].rgbtGreen*Gx[k][l];

                    Yred += copy[k-1+i][l-1+j].rgbtRed*Gy[k][l];
                    Yblue += copy[k-1+i][l-1+j].rgbtBlue*Gy[k][l];
                    Ygree += copy[k-1+i][l-1+j].rgbtGreen*Gy[k][l];

                    /*Xred += copy[k][l].rgbtRed*Gx[k-i+2][l-j+2];
                    Xblue += copy[k][l].rgbtBlue*Gx[k-i+2][l-j+2];
                    Xgreen += copy[k][l].rgbtGreen*Gx[k-i+2][l-j+2];

                    Yred += copy[k][l].rgbtRed*Gy[k-i+2][l-j+2];
                    Yblue += copy[k][l].rgbtBlue*Gy[k-i+2][l-j+2];
                    Ygree += copy[k][l].rgbtGreen*Gy[k-i+2][l-j+2];*/
                }
            }
            red=sqrt(pow(Xred,2)+pow(Yred,2));
            green=sqrt(pow(Xgreen,2)+pow(Ygree,2));
            blue=sqrt(pow(Xblue,2)+pow(Yblue,2));

            int average = round((red + green + blue)/3.0);

            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
            image[i][j].rgbtBlue = average;
        }
    }

    return;
}


void edges(int height, int width, RGBTRIPLE image[height][width])
{
    int Xred; int Xgreen; int Xblue;
    int Yred; int Ygree; int Yblue;

    int Gx[3][3]=
    {
        {-1,0,1},
        {-2,0,2},
        {-1,0,1}
    };
    int Gy[3][3]=
    {
        {-1,-2,-1},
        {0,0,0},
        {1,2,1}
    };
    RGBTRIPLE copy[height][width];
    for (int i =0; i< height; i++) // make  copy // [columns][rows]
    {
        for (int j = 0; j<width; j++)
        {
            copy[i][j]=image[i][j];
        }
    }

    for (int i = 0; i<height; i++)
    {
        for (int j = 0; j<width; j++)
        {
            Xred=0;Xblue=0;Xgreen=0;
            Yred=0; Ygree=0; Yblue=0;
            for(int k=0;k<3; k++) // inner loop for getting 3x3 array
            {
                for(int l = 0; l<3; l++)
                {
                    if(k-1+i>=0 && k-1+i<height && l+j-1 >= 0 && l+j-1<width)
                    {
                    Xred += copy[k-1+i][l-1+j].rgbtRed*Gx[k][l];
                    Xblue += copy[k-1+i][l-1+j].rgbtBlue*Gx[k][l];
                    Xgreen += copy[k-1+i][l-1+j].rgbtGreen*Gx[k][l];

                    Yred += copy[k-1+i][l-1+j].rgbtRed*Gy[k][l];
                    Yblue += copy[k-1+i][l-1+j].rgbtBlue*Gy[k][l];
                    Ygree += copy[k-1+i][l-1+j].rgbtGreen*Gy[k][l];
                    }
                }
            }

            image[i][j].rgbtRed=round(sqrt((Xred*Xred)+(Yred*Yred)));
            image[i][j].rgbtGreen=round(sqrt((Xgreen*Xgreen)+(Ygree*Ygree)));
            image[i][j].rgbtBlue=round(sqrt((Xblue*Xblue)+(Yblue*Yblue)));
            if(round(sqrt((Xred*Xred)+(Yred*Yred)))>255)
            {
                image[i][j].rgbtRed=255;
            }
            if(round(sqrt((Xgreen*Xgreen)+(Ygree*Ygree)))>255)
            {
                image[i][j].rgbtGreen=255;
            }
            if(round(sqrt((Xblue*Xblue)+(Yblue*Yblue)))>255)
            {
                image[i][j].rgbtBlue=255;
            }

        }
    }

    return;
}
