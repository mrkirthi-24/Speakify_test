import ssl
from bs4 import BeautifulSoup
import urllib.request

context = ssl._create_unverified_context()

# Construct the URL for the Google search
search_query = "samsung"
search_query = search_query.replace(" ", "+")
url = f"https://www.google.com/search?q={search_query}"

# User-Agent header to mimic a web browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.99 Safari/537.36"
}

# Create a Request object with headers
req = urllib.request.Request(url, headers=headers)

try:
    response = urllib.request.urlopen(req, context=context)
    # Now you can read the response data
    data = response.read().decode("utf-8")
    soup = BeautifulSoup(data, "html.parser")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
