import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re

# Linkitys artistien Spotify -sivuille

# In Flames
url = 'https://open.spotify.com/artist/57ylwQTnFnIhJh4nu4rxCs'

# Architects
#url = 'https://open.spotify.com/artist/3ZztVuWxHzNpl0THurTFCv'

# Atlas
# url = 'https://open.spotify.com/artist/33BnCqtsMZSw7LlPBwzmmH'

response = requests.get(url)
albumTagList = []
albums = []
print(response)

soup = BeautifulSoup(response.text, "html.parser")
atags = soup.findAll('a')

# Muunnetaan bs4 elementti stringiksi jatkokäsittelyä varten
atags_str = str(atags)

# Yhdistetään elementit
tempList = "".join(atags_str)

# Otetaan talteen linkkien sisältö, joista karsitaan pois kaikki paitsi linkit joiden href on album, 
# jolloin saadaan vain tarvittava tieto
tempList = re.findall(r"<a.*?>", tempList)
for tag in tempList:
    if re.search(r"\/album", tag):
        albumTagList.append(tag)

# Halutaan talteen vain albumien nimet, albumin nimi esiintyy alt parametrissä
# heataan sanaa joka esiintyy merkkien: alt=" jälkeen ja loppuu: " merkkiin
# Lopuksi karsitaan viimeinen " merkki ja tallennetaan albumin nimi albums listaan
for line in albumTagList:
    name = re.search(r'(?<=alt=")(.*?")', line, re.MULTILINE)
    albums.append(name.group(1)[:-1])

    
for album in albums:
    print(album)

