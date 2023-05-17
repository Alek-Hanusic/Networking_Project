import sys
import http.client

def parse_headers(headers):
    parsed_headers = {}
    for header in headers:
        key, value = header.split(': ', 1)
        parsed_headers[key.lower()] = value
    return parsed_headers

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

def display_links(links):
    print("Links:")
    for i, link in enumerate(links):
        print(f"{i + 1}. {link}")

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

        return response_data
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