#! /usr/bin/env python

try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError
import os
from bs4 import BeautifulSoup
import re
import Crop

NUMBER_PAGES = 6 #Introduce the number of pages that your profile has
USERNAME = 'huescacity' #Username in todocoleccion.net
IMAGES_DIRECTORY = "downloadedImages" #Directory name

links_formatted = [] #List of tuples following this pattern (NAME OF THE PIC, path to be saved)

for page in range(1, NUMBER_PAGES+1):  #Get all image links from the different pages and append them in the links_formatted list
    list_href = []
    list_names = []
    url = 'http://www.todocoleccion.net/s/catalogo-antiguedades-arte-coleccionismo-subastas?P=' + str(page) + '&idvendedor=' +USERNAME


    html_page = urlopen(url)
    soup = BeautifulSoup(html_page,"html.parser")
    for link in soup.findAll('a'):
        list_href.append(link.string)

    for name in list_href:
        try:
            if sum(1 for c in name if c.isupper()) > 6:
                list_names.append(name)
        except:
            pass

    website = urlopen(url)
    html = website.read()

    links = re.findall(b'"((http|ftp)s?://.*jpg)"', html)
    for idx,item in enumerate(links):
        links_formatted.append((item[0],list_names[idx])) #format


try:
    os.mkdir(IMAGES_DIRECTORY) #Create directory /downloadImages
except:
    pass

#Proceed to download all files
for idx,download_file in enumerate(links_formatted):
    repeated_file = 1
    print("Downloading file " + str(idx+1) + " of " + str(len(links_formatted)) + " ------- " + download_file[1])
    removed_slash = download_file[1].replace("/", "")
    file_name = IMAGES_DIRECTORY + '/' + removed_slash +'.jpg'

    if os.path.isfile(file_name): # Check if the file is already in the folder and add a (1)
        file_name = IMAGES_DIRECTORY + '/'  +removed_slash + '_('+ str(repeated_file) + ')' + '.jpg'
        repeated_file +=1

    urlx = download_file[0].decode("utf-8")
    f = urlopen(urlx)

    data = f.read()
    with open(file_name, "wb") as code:
        code.write(data)
    Crop.cropImage(file_name)



