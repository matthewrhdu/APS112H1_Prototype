#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <time.h>

#ifndef PORT
#define PORT 54321
#endif

void file_writer(char *data, int size, FILE *file, int start){
    int end = time(NULL);
    int curr = 2 * (end  - start);

    // printf("writing = %s\n", loc + 1);
    fwrite(data, strlen(data), sizeof(char), file);
    fwrite(",", 1, sizeof(char), file);
    fprintf(file, "%d", curr);
    fwrite("\n", 1, sizeof(char), file);
    fflush(file);
}

int main() {
    // create socket
    int listen_soc = socket(AF_INET, SOCK_STREAM, 0);
    if (listen_soc == -1) {
        perror("server: socket");
        exit(1);
    }

    //initialize server address    
    struct sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(PORT);  
    memset(&server.sin_zero, 0, 8);
    server.sin_addr.s_addr = INADDR_ANY;

    // bind socket to an address
    if (bind(listen_soc, (struct sockaddr *) &server, sizeof(struct sockaddr_in)) == -1) {
        perror("server: bind");
        close(listen_soc);
        exit(1);
    } 

    // Set up a queue in the kernel to hold pending connections.
    if (listen(listen_soc, 5) < 0) {
        // listen failed
        perror("listen");
        exit(1);
    }

    printf("connected\n");
    struct sockaddr_in client_addr;
    unsigned int client_len = sizeof(struct sockaddr_in);
    client_addr.sin_family = AF_INET;

    fd_set allset;
    fd_set read_set;

    FD_ZERO(&allset);
    FD_SET(listen_soc, &allset);

    int num_socs = listen_soc;

    char line[35];
    int nready;
    int client_socket;
    int i;

    FILE *file = fopen("database.db", "a");

    int starttime = time(NULL);

    while (1){
        read_set = allset;

        nready = select(num_socs + 1, &read_set, NULL, NULL, NULL);

        if (nready == -1) {
            perror("select");
            continue;
        }

        if (FD_ISSET(listen_soc, &read_set)){
            printf("a new client is connecting\n");
            
            if ((client_socket = accept(listen_soc, (struct sockaddr *)&client_addr, &client_len)) < 0) {
                perror("accept");
                exit(1);
            }
            
            FD_SET(client_socket, &allset);

            // printf("connection from %s\n", inet_ntoa(client_addr.sin_addr));
            if (read(client_socket, line, 35) == -1){
                perror("read");
                exit(1);
            }

            file_writer(line, strlen(line), file, starttime);
            if (write(client_socket, "w", 2) == -1){
                perror("write");
                exit(1);
            }

            for (i = 0; i < 35; i++){
                line[i] = '\0';
            }

            FD_CLR(client_socket, &allset);
            close(client_socket);
        }
    }
    
    close(listen_soc);
    fclose(file);
    printf("finished\n");
    return 0;
}

