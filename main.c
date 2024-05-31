#include <stdio.h>
const char *kw[11] = {"program", "unit", "uses", "interface", "function", "procedure", "implementation", "begin", "end",
                      "var", ";"};

int main()
{
    printf(kw[0]);
    return 0;
}