import os
from BeautifulSoup import BeautifulSoup
import urllib2
import urllib

import re

NUMBER_PAGES = 6 #Introduce the number of pages that your profile has
USERNAME = 'huescacity' #Username in todocoleccion.net

links_formatted = [] #List of tuples following this pattern (NAME OF THE PIC, path to be saved)

for page in range(1, NUMBER_PAGES+1):  #Get all image links from the different pages and append them in the links_formatted list
    list_href = []
    url = 'http://www.todocoleccion.net/s/catalogo-antiguedades-arte-coleccionismo-subastas?P=' + str(page) + '&idvendedor=' +USERNAME

    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page)
    for link in soup.findAll('a'):
        list_href.append(link.string)

    list_names = []
    for name in list_href:
        try:
            if sum(1 for c in name if c.isupper()) > 6:
                list_names.append(name)
        except:
            pass

    website = urllib2.urlopen(url)
    html = website.read()

    links = re.findall('"((http|ftp)s?://.*jpg)"', html)

    for idx,item in enumerate(links):
        links_formatted.append((item[0],list_names[idx]))

try:
    os.mkdir("downloads")
except:
    pass

#Proceed to download all files
for idx,download_file in enumerate(links_formatted):
    print("Downloading file " + str(idx+1) + " of " + str(len(links_formatted)) + " ------- " + download_file[1])
    removed_slash = download_file[1].replace("/", "")
    urllib.urlretrieve(download_file[0], 'downloads/' +removed_slash+'.jpg')