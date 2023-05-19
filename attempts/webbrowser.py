import re
from attempts.connection_helper import HttpConnectionHelper

def main():
    connection_helper = HttpConnectionHelper()

    # Asks for the URL and splits it into host and path
    host = input("Enter the desired URL: ")
    path = "/"

    while True:
        connection_helper.connect(host)
        connection_helper.send_request(f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n".encode('utf-8'))
        response = connection_helper.receive_response()

        # Parse and display response headers
        headers, body = response.split("\r\n\r\n", 1)
        header_lines = headers.split("\r\n")[1:]
        header_dict = dict(line.split(": ", 1) for line in header_lines)
        print("Response headers:")
        for key, value in header_dict.items():
            print(f"{key}: {value}")

        # Parse and display links
        links = re.findall(r'<a href="(.*?)">(.*?)</a>', body)
        print("\nLinks:")
        for i, (url, text) in enumerate(links, start=1):
            print(f"{i}. {text} -> {url}")

        # User input to select a link or exit
        user_input = input("\nEnter the number of the link to follow or 0 to exit: ")
        if user_input == "0":
            break
        else:
            try:
                link_number = int(user_input)
                if 1 <= link_number <= len(links):
                    path = links[link_number - 1][0]
                else:
                    print("Invalid input. Please enter a valid link number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    connection_helper.close()

if __name__ == "__main__":
    main()