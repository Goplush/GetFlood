Based on BUPT 王东滨's sample code

has three parameters

- -t: target IP
- -p: target port, default 80
- -x: thread number, default 250

Using `scapy` to create a TCP connection and send HTTP GET repeatedly

However, it will expose your true IP to server, **SO DON'T USE IT ON REAL SERVER!!! **