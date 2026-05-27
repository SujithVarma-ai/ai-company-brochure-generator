import requests
from bs4 import BeautifulSoup

def fetch_website_contents(url):

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    return soup.get_text()


def fetch_website_links(url):

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    links = []

    for link in soup.find_all("a"):

        href = link.get("href")

        if href:
            links.append(href)

    return links
