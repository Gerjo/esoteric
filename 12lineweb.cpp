#include <cstdlib>
#include <thread>
#include <iostream>
#include <cstring>
#include <unistd.h>
#include <netdb.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <sys/socket.h>
#include <arpa/inet.h>


int main() {
    int sock = ::socket(AF_INET, SOCK_STREAM, 0);

    ::setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, new int(1), sizeof(int));
    sockaddr_in serv_addr = {AF_INET, htons(8989), INADDR_ANY};
    ::bind(sock, (sockaddr *) &serv_addr, sizeof(serv_addr));
    ::listen(sock, 5);

    do {
        sockaddr_in cli_addr;
        socklen_t clilen = sizeof(cli_addr);
        int in           = ::accept(sock, reinterpret_cast<sockaddr*>(&cli_addr), &clilen);

        std::thread([&in]()  {
            int r = ::send(in, "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\nHello there.", 62, 0);
            ::close(in);
        }).detach();


    } while(true);

}


