#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>    /* Internet domain header */
#include <netdb.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <sys/wait.h>

#ifndef PORT
#define PORT 54321
#endif

#define LINE_LENGTH 1024

int main(int argc, char **argv) {
    if (argc != 2){
        fprintf(stderr, "usage: ./client <filename>\n");
        exit(1);
    }

    char query[11];
    strncpy(query, argv[1], 5);
    query[5] = '-';
    
    char write_data[1024];
    strncpy(write_data, argv[1], strlen(argv[1]));
    write_data[strlen(argv[1])] = ' ';
    write_data[strlen(argv[1]) + 1] = '\0';

    FILE *file = fopen(argv[1], "r");
    if (file == NULL){
        perror("fopen");
        exit(1);
    }

    //initialize server address    
    struct sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(PORT);  
    memset(&server.sin_zero, 0, 8);
    
    struct addrinfo *ai;
    char *hostname = "127.0.0.1";

    /* this call declares memory and populates ailist */
    getaddrinfo(hostname, NULL, NULL, &ai);
    server.sin_addr = ((struct sockaddr_in *) ai->ai_addr)->sin_addr;

    // free the memory that was allocated by getaddrinfo for this list
    freeaddrinfo(ai);
    
    char data[LINE_LENGTH];
    for (int t = 0; t < 1000; t++){
        // create socket
        int soc = socket(AF_INET, SOCK_STREAM, 0);
        if (soc == -1) {
            perror("client: socket");
            exit(1);
        }

        int ret = connect(soc, (struct sockaddr *)&server, sizeof(struct sockaddr_in));
        if (ret == -1) {
            perror("client: connect");
            exit(1);
        }

        fscanf(file, "%s\n", data);

        strncat(write_data, data, 35);
        write_data[35] = '\0';

        printf("writing: %s\n", write_data);
        write(soc, write_data, 35 * sizeof(char));

        for (int a = 0; a < strlen(data); a++){
            write_data[strlen(argv[1]) + a + 1] = '\0';
        }

        char dump[2];
        read(soc, dump, 2);
        sleep(1);
        close(soc);
    }

    fclose(file);
    return 0;
}

 