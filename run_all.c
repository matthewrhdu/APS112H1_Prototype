#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

int main(){
    for (int n = 0; n < 5; n++){
        int r = fork();

        if (r == 0){
            char filename[] = "data_.csv";
            filename[4] = '1' + n;

            execlp("./client", "client", filename, NULL);
            perror("execlp");
            exit(1);
        }
        usleep(0.5 * 1e6);
    }

    return 0;
}

