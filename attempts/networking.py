import re
import socket
import ssl

#!/usr/bin/env python3
# This module defines general functions for establishing an arbitrary TCP connection with a remote host

import socket
import ssl


class HttpConnectionHelper:
    """
    Helper class for establishing a TCP connection
    """

    def __init__(self):
        """
        Constructor
        """
        self.internal_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port=80, secure=False):
        """
        Establishes a connection
        :return:
        """
        connection_port = port
        if secure:
            connection_port = 443
        self.internal_connection.connect((host, connection_port))
        if secure:
            self.internal_connection = ssl.wrap_socket(self.internal_connection, keyfile=None, certfile=None,
                                                       server_side=False, cert_reqs=ssl.CERT_NONE,
                                                       ssl_version=ssl.PROTOCOL_SSLv23)

    def send_request(self, request):
        """
        Sends an arbitrary request
        :param request: The request to send (as text)
        :return:
        """
        self.internal_connection.send(request.encode())

    def receive_response(self):
        """
        Waits and receives a response form the server
        :return:
        """
        return repr(self.internal_connection.recv(4096))

    def close(self):
        """
        Closes the connection
        :return:
        """
        self.internal_connection.close()


if __name__ == "__main__":
    connection_helper = HttpConnectionHelper()
    connection_helper.connect("www.google.at", 443, True)
    connection_helper.send_request("HEAD / HTTP/1.1\r\nHost: www.google.at\r\n\r\n")
    response = connection_helper.receive_response()
    http_response_headers = repr(response)
    print(http_response_headers)

def get_links_from_html(html_content):
    link_pattern = re.compile(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', re.IGNORECASE)
    links = link_pattern.findall(html_content)
    numbered_links = [(index + 1, text, href) for index, (href, text) in enumerate(links)]
    return numbered_links

def main():
    url = "www.example.com"
    connection_helper = HttpConnectionHelper()
    connection_helper.connect(url, 80, False)
    connection_helper.send_request(f"GET / HTTP/1.1\r\nHost: {url}\r\n\r\n")
    response = connection_helper.receive_response()
    connection_helper.close()

    response_lines = response.split('\\r\\n')
    headers = {}
    html_content = ""
    in_headers = True
    for line in response_lines:
        if in_headers:
            if line == '':
                in_headers = False
            else:
                parts = line.split(': ', 1)
                if len(parts) == 2:
                    key, value = parts
                    headers[key] = value
        else:
            html_content += line

    print("HTTP Response Headers:")
    for key, value in headers.items():
        print(f"{key}: {value}")

    links = get_links_from_html(html_content)
    print("\nLinks:")
    for index, text, href in links:
        print(f"{index}. {text} -> {href}")

    while True:
        try:
            selected_link = int(input("\nEnter the number of the link you want to visit (0 to exit): "))
            if selected_link == 0:
                break
            elif 1 <= selected_link <= len(links):
                _, _, target_url = links[selected_link - 1]
                print(f"Visiting: {target_url}")
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()