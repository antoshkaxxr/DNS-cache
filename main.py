import socket
from bytes_sequence_reader import BytesSequenceReader


class DNSServer:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 53
        self.root_nameserver = '198.41.0.4'

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind((self.host, self.port))

            print(f"DNS-сервер запущен и слушает {self.host}:{self.port}")
            print("")
            print("Откройте новое окно командной строки/терминала и введите команду:")
            print("dig example.com A @127.0.0.1")
            print("")

            while True:
                data, client_address = server_socket.recvfrom(1024)
                print("Отправляю запрос NS-серверам...")
                response = self.process_request(data)
                print("Формирую ответ...")
                server_socket.sendto(response, client_address)

    def process_request(self, request):
        reader = BytesSequenceReader(bytearray(request))
        dns_request = reader.read_message()
        if not dns_request.question:
            return
        response = self.query_nameservers(dns_request)
        return response

    def query_nameservers(self, dns_request):
        server = self.root_nameserver
        servers = [server]
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while servers:
            client_socket.sendto(dns_request.req_to_bytearray(), (server, self.port))
            response, _ = client_socket.recvfrom(1024)
            print(f'Произошло обращение к {server}')
            reader = BytesSequenceReader(bytearray(response))
            dns_response = reader.read_message()

            for answer in dns_response.answer:
                if answer.TYPE == 1:
                    return response

            for data in (dns_response.authority, dns_response.additional):
                for item in data:
                    if item.TYPE == 1:
                        servers.append('.'.join(str(part) for part in bytearray(item.RDATA)))

            if servers:
                server = servers.pop(0)
                if server == self.root_nameserver:
                    server = servers.pop(0)


if __name__ == '__main__':
    dns_server = DNSServer()
    dns_server.start()
