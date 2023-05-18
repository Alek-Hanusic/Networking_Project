#!/usr/bin/env python3
# This module defines general functions for establishing an arbitrary TCP connection with a remote host

import socket
import ssl
import sys


class HttpConnectionHelper:
    """
    Helper class for establishing a TCP connection
    """

    def __init__(self):
        """
        Constructor
        """
        self.internal_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # AF_INET (fist argument) --> constant, which represents the address (and protocol) families
    # SOCK_STREAM (second argument) --> constant, which represents the socket types

    def connect(self, host, port=80, secure=False):
        """
        Establishes a connection
        :return:
        """
        connection_port = port
        if secure:
            connection_port = 80
        self.internal_connection.connect((host, connection_port))
        if secure and False:
            self.internal_connection = ssl.wrap_socket(self.internal_connection, keyfile=None, certfile=None,
                                                       server_side=False, cert_reqs=ssl.CERT_NONE,
                                                       ssl_version=ssl.PROTOCOL_SSLv23)

    def send_request(self, request):
        """
        Sends an arbitrary request
        :param request: The request to send (as text)
        :return:
        """
        self.internal_connection.send(request)

    def receive_response(self):
        """
        Waits and receives a response form the server
            :return: string representation of the server response
        """
        return str(self.internal_connection.recv(4096), 'utf-8')

    def close(self):
        """
        Closes the connection
            :return:
        """
        self.internal_connection.close()

    def browse_website_links(self, website):
        """
        We find the links in the example.html
            :param website: The body of html code
            :return: The found links in the html website
        """
        length = len(website)
        begin = 0  # where we start the search
        found_links = []
        while website.find('a href', begin, length) != -1:  # until there is no links in the html document
            a = website.find('a href', begin, length)  # we search for the links in html, which have a href in front
            a = a + 7
            b = website.find('>', a, length)
            # get rid of additional spaces and "
            link = website[a:b].strip()
            link = link.strip('"')
            link = link.strip()
            found_links.append(link)  # the found links are appended
            begin = b  # start searching from the end of the currently found link
        return found_links

    def return_found_links(self, links_found):
        """
        Returns the text with numbered links found
            :param links_found: The list of links found in the website
            :return: The text to be displayed made out of links
        """
        x = 1
        text = ''
        for i in range(len(links_found)):
            link = f'[{x}] Link {x} -> {links_found[i]}\n'
            x += 1  # variable increases so we go through the whole list
            text = text + link  # returns the text
        return text

    def print_response_head(self, head):
        """
        Function is of type void and only prints the part of the response needed
            :param head: String containing response header
        """
        start = head.find('Server')  # find from where the response will be printed
        print(head[start:])  # we print the response needed


if __name__ == "__main__":
    web_url = sys.argv[1]  # web_url will be the argument from cmd when we run this program
    [host, file_path] = web_url.split("/", 2)

    while True:
        connection_helper = HttpConnectionHelper()
        connection_helper.connect(host, 80, True)  # secure connection to host
        connection_helper.send_request(f"GET /{file_path} HTTP/1.1\r\nHost: {host}\r\n\r\n".encode('utf-8'))
        response_head = connection_helper.receive_response()  # response to get the head
        connection_helper.print_response_head(response_head)
        response_body = connection_helper.receive_response()  # html
        web_links = connection_helper.browse_website_links(response_body)  # find the links in the html code
        formatted_links = connection_helper.return_found_links(web_links)  # display the links found in html code
        print(formatted_links)  # we print the links needed

        command_text = input('Press 0 to exit or number of the link:')
        # get the users input if he wants to see the link or to exit
        if command_text == '0':
            break
        else:
            if int(command_text) > len(web_links):  # if the input is too big (bigger than the links found)
                print('Wrong input (the number is too big).\n')
            else:
                file_path = web_links[int(command_text) - 1]
