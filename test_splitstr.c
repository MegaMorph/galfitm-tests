#include <stdio.h>
#include <string.h>

void splitstr (char string[], char *tokens[], char delim[], int nmax);

int main (int argc, char *argv[])
{
  int nmax=16;
  char string[] = "hello there, steven, blah,blah,blah";
  char * s[nmax];

  splitstr(string, s, " ,", nmax);

  strcpy(string, "I ate it!");

  int i = 0;
  while (s[i] != NULL) 
    printf("%s\n", s[i++]);

  printf("This many strings: %i\n", i);

}
