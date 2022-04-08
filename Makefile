all : server client run_all

PORT = 52035

client : client.o
	gcc -Wall -g -DPORT=${PORT} -o client client.o

server : server.o
	gcc -Wall -g -DPORT=${PORT} -o server server.o

clear_database : database.db
	> database.db

data1.csv_db :
	touch data1.csv_db

run_all : run_all.o
	gcc -Wall -g -o run_all run_all.o

%.o : %.c
	gcc -Wall -g -c $^

clear : clear_database
	rm *.o
	rm run_all
	rm server
	rm client
