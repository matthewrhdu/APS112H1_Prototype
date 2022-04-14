all : server client run_all

PORT = 52035

client : client.c
	gcc -Wall -g -DPORT=${PORT} -o client client.c

server : server.c
	gcc -Wall -g -DPORT=${PORT} -o server server.c

clear_database : database.db
	> database.db

run_all : run_all.c
	gcc -Wall -g -o run_all run_all.c

clear : clear_database
	rm *.o
	rm run_all
	rm server
	rm client
