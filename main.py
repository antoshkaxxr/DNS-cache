import threading
import socket
import time
from bytes_sequence_reader import BytesSequenceReader
from cache_worker import CacheWorker


class DNSRecord:
    def __init__(self, response, expiration_time):
        self.response = response
        self.expiration_time = expiration_time


class DNSServer:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 53
        self.root_nameserver = '198.41.0.4'
        self.server_socket = None
        self.cache_worker = CacheWorker()

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))

        print(f"DNS-сервер запущен и слушает {self.host}:{self.port}")
        print("")
        print("Откройте новое окно командной строки/терминала и введите команду:")
        print("dig example.com A @127.0.0.1")
        print("")

        while True:
            data, client_address = self.server_socket.recvfrom(1024)
            thread = threading.Thread(target=self.handle_request, args=(data, client_address))
            thread.start()

    def handle_request(self, data, client_address):
        print("Отправляю запрос NS-серверам...")
        response = self.process_request(data)
        print("Формирую ответ...")
        print("")
        self.server_socket.sendto(response, client_address)

    def process_request(self, request):
        reader = BytesSequenceReader(bytearray(request))
        dns_request = reader.read_message()
        if not dns_request.question:
            return
        cached_response = self.cache_worker.get_cached_response(dns_request)
        if cached_response:
            print("Ответ получен из кэша.")
            response = self.replace_request_id(cached_response, dns_request.header.ID)
            return response
        response = self.query_nameservers(dns_request)
        if response:
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
                    cache_key = str(dns_request.question[0].QNAME)
                    expiration_time = time.time() + answer.TTL
                    self.cache_worker.cache[cache_key] = DNSRecord(response, expiration_time)
                    self.cache_worker.save_cache()
                    return response

            for data in (dns_response.authority, dns_response.additional):
                for item in data:
                    if item.TYPE == 1:
                        servers.append('.'.join(str(part) for part in bytearray(item.RDATA)))

            if servers:
                server = servers.pop(0)
                if server == self.root_nameserver:
                    server = servers.pop(0)

    @staticmethod
    def replace_request_id(response, new_id):
        header_id = new_id.to_bytes(2, byteorder='big')
        return header_id + response[2:]


if __name__ == '__main__':
    dns_server = DNSServer()
    dns_server.start()
