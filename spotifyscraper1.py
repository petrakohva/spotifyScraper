import requests
import urllib.request
import time
import re
from datetime import datetime

startTime = datetime.now()

# Listat
# lista johon kerätään linkkien sisältö
aTagList = []

# Lista johon kerätään linkkilistasta albumiin viittavat rivit
albumTagList = []

# Lista johon kerätään vain albumin nimitieto
albumNameList = []


# Linkitys artistien Spotify -sivuille
# In Flames
url = 'https://open.spotify.com/artist/57ylwQTnFnIhJh4nu4rxCs'

# Architects
#url = 'https://open.spotify.com/artist/3ZztVuWxHzNpl0THurTFCv'

# Atlas
# url = 'https://open.spotify.com/artist/33BnCqtsMZSw7LlPBwzmmH'

# haetaan urlin mukaista verkkosivua ja kirjoitetaan sivun data muuttujaan
response = requests.get(url)
data = response.text

# Otetaan talteen linkkien sisältö aTagListaan, joista karsitaan pois kaikki paitsi linkit joiden href on album, 
# jolloin saadaan vain tarvittava tieto albumTagListaan
aTagList = re.findall(r"<a.*?>", data)
for tag in aTagList:
    if re.search(r"\/album", tag):
        albumTagList.append(tag)

# Halutaan talteen vain albumien nimet, albumin nimi esiintyy alt parametrissä
# heataan sanaa joka esiintyy merkkien: alt=" jälkeen ja loppuu ensimmäiseen: " merkkiin
# Lopuksi karsitaan viimeinen " merkki ja tallennetaan albumin nimi albums listaan
for line in albumTagList:
    name = re.search(r'(?<=alt=")(.*?")', line, re.MULTILINE)
    albumNameList.append(name.group(1)[:-1])

# Tulostetaan albumien nimet
for album in albumNameList:
    print(album)
print(datetime.now() - startTime)
