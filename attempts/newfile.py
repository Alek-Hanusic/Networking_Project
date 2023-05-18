import socket
import ssl
import sys

class ConnectionHelper:
    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def establish_connection(self, host, port=80, secure=False):
        connection_port = 80 if not secure else port
        self.connection.connect((host, connection_port))
        if secure:
            self.connection = ssl.wrap_socket(self.connection)

    def send_request(self, request):
        self.connection.send(request.encode('utf-8'))

    def receive_response(self):
        return str(self.connection.recv(4096), 'utf-8')

    def close_connection(self):
        self.connection.close()

    @staticmethod
    def find_links(website):
        return [link.strip().strip('"').strip() for link in website.split('a href=')[1:]]

    @staticmethod
    def format_links(links):
        return '\n'.join(f'[{i+1}] Link {i+1} -> {link}' for i, link in enumerate(links))

    @staticmethod
    def print_response_header(header):
        for line in header.splitlines():
            if line.startswith('Server'):
                print(line)
                break

if __name__ == "__main__":
    web_url = sys.argv[1]
    if "/" not in web_url:
        print("Invalid URL: must contain a forward slash")
        sys.exit(1)

    host, file_path = web_url.split("/", 1)
    while True:
        connection_helper = ConnectionHelper()
        connection_helper.establish_connection(host, 80, True)
        connection_helper.send_request(f"GET /{file_path} HTTP/1.1\r\nHost: {host}\r\n\r\n")
        response_header = connection_helper.receive_response()
        connection_helper.print_response_header(response_header)
        response_body = connection_helper.receive_response()
        web_links = connection_helper.find_links(response_body)
        formatted_links = connection_helper.format_links(web_links)
        print(formatted_links)
        command_text = input('Press 0 to exit or enter the number of the link: ')
        if command_text == '0':
            break
        else:
            if int(command_text) > len(web_links):
                print('Wrong input (the number is too big).\n')
            else:
                file_path = web_links[int(command_text) - 1]