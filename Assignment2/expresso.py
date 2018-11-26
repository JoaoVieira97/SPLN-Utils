import re
import sys
import os
import html
from urllib.request import urlretrieve
from unidecode import unidecode
import requests
import latex_utils

def pesquisarNoticias(argument, f_descriptor):
    print("Termo de pesquisa: " + argument)
    payload = {'query':argument}
    r = requests.get('https://www.publico.pt/pesquisa', params = payload)
    print('URL de pesquisa = ' + r.url + '\n')
    links = re.findall(r'<div class="media-object-section">[\n\s]*<a href="(.*)">', r.text)
    obterNoticias(links, f_descriptor)
