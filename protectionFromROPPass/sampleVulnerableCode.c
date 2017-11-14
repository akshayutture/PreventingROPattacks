
// Reference - http://codearcana.com/posts/2013/05/28/introduction-to-return-oriented-programming-rop.html
#include <stdio.h>
#include <string.h>

void not_called() {
    printf("Enjoy your shell!\n");
    system("/bin/bash");
}

void vulnerable_function(char* string) {
    char buffer[100];
    strcpy(buffer, string);
}

int main(int argc, char** argv) {
    vulnerable_function(argv[1]);
    printf("Main completed\n");
    return 0;
}
