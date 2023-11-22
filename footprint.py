import requests
import os
import sys
import validators


def fetch_headers(given_url):
    """Fetching the headers from the given URL(s)"""

    headers_dict = {}   # The dictionary will store the URL(s) and the header(s) retrieved by the request.

    if os.path.isfile(given_url):   # Checking if the passed argument is a file:

        urls = []

        with open(f"{os.path.abspath(given_url)}", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line != "\n":
                    urls.append(line.strip())

        file.close()

        for url in urls:

            if not validators.url(url):
                print(f"{url} is an invalid url to be used.\n\n")
                exit(3)

            page = requests.get(url)

            if page.status_code != 200:
                page.raise_for_status()
                exit(4)

            headers_dict[url] = page.headers

    else:   # If the passed argument is not a file, it means it's just a single URL:

        if not validators.url(given_url):
            print(f"{given_url} is an invalid url to be used.\n\n")
            exit(3)

        page = requests.get(given_url)

        if page.status_code != 200:
            page.raise_for_status()

        headers_dict[given_url] = page.headers

    return headers_dict


def processing_headers(given_header):
    """Processing the output for the URL(s) header(s)"""

    for url, header in given_header.items():

        print("\n")
        print(f"{'*' * len(url)}****************")
        print(f"* {url} - Footprint *")
        print(f"{'*' * len(url)}****************\n\n")
        print("-------------------------------------------------------------------------------------------------------")
        print("\n")
        for key, value in header.items():

            print(f"{key}: \n\t{value}\n")

        print("-------------------------------------------------------------------------------------------------------")
        print("\n")


def main():

    msg = "Please enter use the file path containing the urls\n"\
          "or enter the a simple url."

    if not sys.argv[1]:
        print(f"Invalid arguments\n\n{msg}")
        exit(1)

    if len(sys.argv) > 2:
        print(f"Too many arguments!\n\n{msg}")
        exit(2)

    headers = fetch_headers(sys.argv[1])

    processing_headers(headers)


if __name__ == "__main__":

    main()
