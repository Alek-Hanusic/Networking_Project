################################################################
# Done by Alek Hanusic & Guram Sikharulidze
################################################################

# We werent sure how to make it run the webserver provided so we just did it for online websites
import re
# import socket
# import ssl
from connection_helper import HttpConnectionHelper
def get_links_from_html(html_content):
    link_pattern = re.compile(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', re.IGNORECASE) #pattern for finding links (case not sensitive)
    links = link_pattern.findall(html_content) #find all links in html content
    numbered_links = [(index + 1, text, href) for index, (href, text) in enumerate(links)] # adds numbers to links and reutrns tuple
    return numbered_links

def main():
    url = input("Enter the desired URL: ") # asks for url
    conn_hlpr = HttpConnectionHelper() #we just assigned the class to a variable
    conn_hlpr.connect(url, 80, False) #connects to the url
    conn_hlpr.send_request(f"GET / HTTP/1.1\r\nHost: {url}\r\n\r\n") #sends request to the url
    response = conn_hlpr.receive_response() #receives response from the url
    conn_hlpr.close() #closes the connection

# extracting headers

    response_lines = response.split('\\r\\n') #this splits the response into lines
    headers = {} # creates empty dictionary
    html_cont = "" # creates empty string
    in_headers = True #default value is true
    for line in response_lines:
        if in_headers:
            if line == '': #if the line is empty string it changes the value of in_headers to false
                in_headers = False
            else:
                parts = line.split(': ', 1) #splits the line into key and value pairs and adds them to the dictionary
                if len(parts) == 2:
                    key, value = parts
                    headers[key] = value
        else:
            html_cont += line #adds the line to the html content

    print("HTTP Response Headers:") #just iterates over items in the headers dictionary and prints them
    for key, value in headers.items():
        print(f"{key}: {value}")

    links = get_links_from_html(html_cont) #calls the function to get links from html content
    print("\nLinks:")
    for index, text, href in links:
        print(f"{index}. {text} -> {href}") #prints the links

    while True: #asks for input and if the input is valid it prints the link
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

if __name__ == "__main__": #runs the main function when it the program is run, could be modified
    main()