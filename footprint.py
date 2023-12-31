import requests
import os
import sys
import validators


def url_eval(url):
    """Evaluating if the URL is valid and making the request."""

    if not validators.url(url):  # Evaluating if it's a valid URL.
        print(f"{url} is an invalid url to be used.\n\n")  # Print an error message in case invalid URL.
        exit(2)  # End the program with status code 3.

    try:

        page = requests.get(url)  # Trying to make a request to the current URL.

    except requests.RequestException:  # In case of any request exceptions:

        print(f"Error: Bad URL request for {url}")  # Printing a message for a Bad Request Error.
        exit(3)  # Ending the program with status code 4.

    if page.status_code != 200:  # Evaluating if the request was successful if the request code is different
        # then 200 (Code for successful request):
        page.raise_for_status()  # Printing an error message with the returned status code.
        exit(4)  # Ending the program execution with status code 5.

    return page


def fetch_headers(given_url):
    """Fetching the headers from the given URL(s)"""

    headers_dict = {}   # The dictionary will store the URL(s) and the header(s) retrieved by the request.

    if os.path.isfile(given_url):   # Checking if the passed argument is a file:

        urls = []   # This list will store the URL(s) from the file passed as an argument.

        with open(f"{os.path.abspath(given_url)}", "r") as file:    # Opening the file.
            lines = file.readlines()    # Read the lines into program memory.
            for line in lines:  # Going through each URL.
                if line != "\n":    # Making sure only valid URL are loaded into the list, ignoring empty lines.
                    urls.append(line.strip())   # Adding the URL into the "urls" lists and removing any extra characters

        file.close()    # Closing the file.

        for url in urls:    # Iterating through each URL into the list

            page = url_eval(url)    # Evaluating if it's a valid URL.

            headers_dict[url] = page.headers    # If the request was successful, adding the url and the url's header to
            # the "headers_dict" dictionary for processing the output message later.

    else:   # If the passed argument is not a file, it means it's just a single URL, therefore:

        page = url_eval(given_url)   # Evaluating if it's a valid URL.

        headers_dict[given_url] = page.headers  # If the request was successful, adding the url and the url's header to
        # the "headers_dict" dictionary for processing the output message later.

    return headers_dict    # Returning the dictionary containing the URL(s) and the Header(s) as key-value pairs,
    # respectively.


def processing_headers(given_header):
    """Processing the output for the URL(s) header(s)"""

    for url, header in given_header.items():    # Iterating through each "url-header" element within the dictionary
        # passed as an argument to the function.

        print("\n")
        print(f"{'*' * len(url)}****************")
        print(f"* {url} - Footprint *")
        print(f"{'*' * len(url)}****************\n\n")
        print("-------------------------------------------------------------------------------------------------------")
        print("\n")

        for key, value in header.items():   # Printing the header's element for the current URL.

            print(f"{key}: \n\t{value}\n")

        print("-------------------------------------------------------------------------------------------------------")
        print("\n")


def main():

    # Error message in case argument errors are detected.
    msg = "Please enter use the file path containing the urls\n"\
          "or enter the a simple url."

    if len(sys.argv) != 2:   # Checking if more than one argument was used.
        print(f"Invalid arguments!\n\n{msg}")  # Printing an error message in case of argument errors.
        exit(1)    # Ending program's execution with status code 2.

    headers = fetch_headers(sys.argv[1])    # Retrieving the header(s) for the URL(s).

    processing_headers(headers)    # Processing the output for the header(s).


if __name__ == "__main__":

    main()  # Executing script.
