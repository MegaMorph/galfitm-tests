#include <stdio.h>
#include <string.h>

void splitstr (char string[], char *tokens[], char delim[], int nmax);

int main (int argc, char *argv[])
{
  int nmax=16;
  char string[] = "123, 4.56,9.87654 3.1412";
  float s[nmax];
  int n, i;

  n = splitstrtofloat(string, s, " ,", nmax);

  strcpy(string, "I ate it!");

  for (i=0; i<n; i++)
    printf("%f\n", s[i]);

  printf("This many floats: %i\n", i);

}
