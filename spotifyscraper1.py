import requests
import urllib.request
import time
import re
import os
from emailsender import sendEmail


# Linkitys artistien Spotify -sivuille
# In Flames
urls = ['https://open.spotify.com/artist/3ZztVuWxHzNpl0THurTFCv', 'https://open.spotify.com/artist/33BnCqtsMZSw7LlPBwzmmH']
txt_file_names = ["Architects.txt", "Atlas.txt"]

# Fuktio joka käyttää parametreina urlia ja tekstitiedoston nimeä
# HUOM url lista ja txtFile lista pitää olla synkissä eli idex paikalla oleva url täytyy viitata esittäjään
# ESIM nyt urls[0] on InFlamesin sivu spotifyssä
def spotifyscraper(url, filename):

# emailpohja
    email_message = """\
Subject: Uutta musiikkia artistilta {artisti}!

Löydetty uusi albumi:  """.format(artisti = filename.rstrip(".txt"))
    
# ~Listat~

# Lista, johon kerätään linkkien sisältö
    aTagList = []

    # Lista, johon kerätään linkkilistasta albumiin viittavat rivit
    albumTagList = []

    # Lista, johon kerätään vain albumin nimitieto, sekä tekstitiedoston lista
    albumsOnSite = []
    albums_in_txtfile = []

    # haetaan urlin mukaista verkkosivua ja kirjoitetaan sivun data muuttujaan
    response = requests.get(url)
    data = response.text

    # Otetaan talteen linkkien sisältö aTagListaan, joista karsitaan pois kaikki
    # paitsi linkit joiden href on album, 
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
        albumsOnSite.append(name.group(1)[:-1])

    with open(filename) as f:
        albums_in_txtfile = f.read().splitlines()

        # Käydään läpi verkkosivulta saatu albumilista ja verrataan sitä tallennettuun albumilistaan
        # Jos jotaikin verkosta ladatuista albumeista ei löydy, niin lähetetään ilmoitus s-postiin ja
        # tallennetaan uusi albumilista
    for album in albumsOnSite:    
        if album not in albums_in_txtfile:
            sendEmail(email_message.encode("utf-8") + "{album}\nLinkki artistin sivulle: {link}".format(link = url, album = album).encode("utf-8"))
            with open(filename, "w") as f:
                for line in albumsOnSite:
                    f.write(line + "\n")

# Ohjelma ajaa kaikki urlit mitä käyttäjä on listannut
# ikuisesti

# runTwicePerDay = 60*60*12
while True:
    i = 0
    print("selaa...")
    for url in urls:
        print(txt_file_names[i].rstrip(".txt"))
        spotifyscraper(url,txt_file_names[i])
        i = i+1
    print("selaus valmis nukkuu 10 sec")
    time.sleep(10)                    
