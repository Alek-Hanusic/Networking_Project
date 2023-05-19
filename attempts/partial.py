import re
import socket
import ssl
from connection_helper import HttpConnectionHelper
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