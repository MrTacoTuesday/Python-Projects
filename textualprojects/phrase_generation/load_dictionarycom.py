

import requests;
from bs4 import BeautifulSoup;

# Send a GET request to the website
word = "a";
url = f'https://dictionary.com/browse/{word.lower()}';
response = requests.get(f'https://dictionary.com/browse/{word.lower()}')

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser');

# Extract data (example: all paragraph texts)

# data-type="dictionary-headword-module"
# data-type="part-of-speech-module"
paragraphs = soup.find_all({});
for p in paragraphs:
    print(p.get_text());