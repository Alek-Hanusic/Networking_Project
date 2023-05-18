import sys
import socket
import re
from urllib.parse import urlparse, urljoin


def send_get_request(url):
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else '/'

    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, 80))
        s.sendall(request.encode())
        response = s.recv(4096).decode()

    return response


def parse_headers(response):
    headers = {}
    header_lines = response.split('\r\n\r\n', 1)[0].split('\r\n')[1:]
    for line in header_lines:
        key, value = line.split(': ', 1)
        headers[key] = value
    return headers


def parse_links(response):
    body = response.split('\r\n\r\n', 1)[1]
    links = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', body)
    return links


def main():
    while True:
        url = input("Enter the URL to open or type 'exit' to quit: ")
        if url.lower() == 'exit':
            break

        response = send_get_request(url)
        headers = parse_headers(response)
        links = parse_links(response)

        print("HTTP Response Headers:")
        for key, value in headers.items():
            print(f"{key}: {value}")

        print("\nLinks:")
        for i, (href, text) in enumerate(links, start=1):
            print(f"{i}. {text.strip()} -> {urljoin(url, href)}")

        while True:
            choice = int(input("\nEnter the number of the link to visit or 0 to go back: "))
            if choice == 0:
                break
            elif 1 <= choice <= len(links):
                url = urljoin(url, links[choice - 1][0])
                response = send_get_request(url)
                headers = parse_headers(response)
                links = parse_links(response)

                print("\nHTTP Response Headers:")
                for key, value in headers.items():
                    print(f"{key}: {value}")

                print("\nLinks:")
                for i, (href, text) in enumerate(links, start=1):
                    print(f"{i}. {text.strip()} -> {urljoin(url, href)}")
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()