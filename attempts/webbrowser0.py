import sys
import http.client


def parse_headers(headers):
    parsed_headers = {}
    for header, value in headers:
        try:
            parsed_headers[header.lower()] = value
        except ValueError:
            print(f"Invalid header format: {header}")
    return parsed_headers


##For the parse_headers function we tried for parses to be the response headers and show that it converts them into
# a dictionary of key-value pairs.
#For the the display_headers function we show that it prints the parsed
# headers in a user-friendly format.nted implementation of a basic
# text-based web browser using HTTP requests.
def display_headers(headers):
    print("Headers:")
    for key, value in headers.items():
        print(f"{key}: {value}")

def parse_links(html):
    links = []
    start_tag = '<a href="'
    end_tag = '"'
    start_index = html.find(start_tag)
    while start_index != -1:
        end_index = html.find(end_tag, start_index + len(start_tag))
        link = html[start_index + len(start_tag):end_index]
        links.append(link)
        start_index = html.find(start_tag, end_index)
    return links
##The provided make_get_request function constructs a proper GET request using the given URL.
# It sends the request to the server and retrieves the response.
def display_links(links):
    print("Links:")
    for i, link in enumerate(links):
        link_num = i + 1
        print(f"[{link_num}] {link} -> {link}")


def make_get_request(url):
    parsed_url = http.client.urlsplit(url)
    host = parsed_url.netloc
    path = parsed_url.path

    connection = http.client.HTTPConnection(host)

    try:
        connection.request("GET", path)
        response = connection.getresponse()

        headers = parse_headers(response.getheaders())
        display_headers(headers)

        response_data = response.read()

        charset = headers.get('content-type', '').split('charset=')[-1]
        if not charset:
            charset = 'utf-8'

        response_text = response_data.decode(charset)

        links = parse_links(response_text)
        display_links(links)

        connection.close()

        # Prompt the user for link selection
        while True:
            user_input = input("Enter the number of the link to follow (0 to exit): ")
            if user_input == '0':
                break

            try:
                link_num = int(user_input)
                if link_num >= 1 and link_num <= len(links):
                    selected_link = links[link_num - 1]
                    make_get_request(selected_link)
                else:
                    print("Invalid link number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid link number.")

    except http.client.HTTPException as e:
        print("An HTTP exception occurred:", e)
    except Exception as e:
        print("An error occurred:", e)

    return None


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        make_get_request(url)
    else:
        print("Please provide a URL as a command-line argument.")
#The code includes comments as you see by us that describe the purpose of each function and relevant code blocks.
#The comments provide explanations for the parameters, variables, and return values where applicable.
#We tried for the code to follow PEP 8 style guidelines for clean and readable code.

#To run the program, save the code in a file named webbrowser.py and
# execute it using the command python webbrowser.py.
# The program will prompt you to enter a URL, and it will display the response headers and links found in the HTML body.
# Please note that the provided code assumes that the server responds with valid HTML and that the links are enclosed
# in <a> tags with the href attribute. Make sure to carefully read the comments within the code to
# understand the purpose of each function and the flow of execution.