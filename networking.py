import http.client

def make_get_request(url):
    # Parse the URL to extract the host and path
    parsed_url = http.client.urlsplit(url)
    host = parsed_url.netloc
    path = parsed_url.path

    # Establish a connection to the host
    connection = http.client.HTTPConnection(host)

    try:
        # Send the GET request
        connection.request("GET", path)

        # Get the response
        response = connection.getresponse()

        # Read the response data
        response_data = response.read().decode("utf-8")

        # Close the connection
        connection.close()

        # Return the response data
        return response_data
    except http.client.HTTPException as e:
        print("An HTTP exception occurred:", e)
    except Exception as e:
        print("An error occurred:", e)

    return None
