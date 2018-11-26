import re
import sys
import os
import html
from urllib.request import urlretrieve
from unidecode import unidecode
import requests
import latex_utils

root_path="https://expresso.sapo.pt/"

def obterNoticias(links, out):
    errors_output = open("errors_output.txt", "w")
    for link in links:
        full_path=root_path+link
        print('A processar ' + link + ' ... ')

        link_content = requests.get(full_path)
        #titulo = re.findall(r'<title>(.*[^\s\n\t\r])\s+\|.*\| PÚBLICO</title>', link_content.text)
        titulo = re.findall(r'<h1 class="headline story__headline">\s*(.*[^\s\n\t\r])[^<]*</h1>', link_content.text)
        if not titulo:
            errors_output.write("Can't get title in " + link + "\n")
            print("Ver erros!\n---------------------------------")
            continue
        description = re.findall(r'<div class="story__blurb lead" itemprop="description">\s*<p>\s*(.*)\s*</p>\s*</div>', link_content.text)
        if not description:
            errors_output.write("Can't get description in " + link + "\n")
            print("Não foi detetada qualquer descrição. Ver erros!")
        images = re.findall(r'data-media-viewer="(.*)"', link_content.text)

        paragrafos = re.findall(r'<div class="story__body" id="story-body">\s*<p>(.*)\s*</p>', link_content.text)
        paragrafos = paragrafos + re.findall(r'<p>\s*(.*)\s*</p>.*\s*.*<aside class=".*">', link_content.text)
        if not paragrafos:
            errors_output.write("Can't get text in " + link + "\n")
            print("Ver erros!\n---------------------------------")
            continue
        
        print(titulo[0])
        tex_folder = ".files/" + ''.join(unidecode(titulo[0]).split(' ')).lower()
        tex_folder = re.sub(r'"',r'',tex_folder)
        os.makedirs(tex_folder, exist_ok=True)

        img_counter=0
        img_paths=[]
        for image in images:
            with open(tex_folder+"/img_"+str(img_counter)+".jpeg", "wb") as im_dump:
                r = requests.get(image)
                for chunk in r.iter_content(chunk_size=128):
                    im_dump.write(chunk)
            img_paths.append("/img_"+str(img_counter)+".jpeg")
            img_counter+=1
        img_paths=[tex_folder+img_name for img_name in img_paths]

        #for paragrafo in paragrafos:
            #print(latex_utils.limparTexto(paragrafo))
        print("Impresso no documento!\n---------------------------------")
        latex_utils.escreverLatex(out, titulo[0], description, img_paths, paragrafos)

def pesquisarNoticias(argument, f_descriptor):
    print("Termo de pesquisa: " + argument)
    payload = {'q':argument}
    r = requests.get('https://expresso.sapo.pt/pesquisa', params = payload)
    print('URL de pesquisa = ' + r.url + '\n')
    #links = re.findall(r'<h1 class="title " itemprop="name">[\n\s]*<a href="(.*)" itemprop="url" rel="canonical">', r.text)
    links = re.findall(r'<a href="(.*)" itemprop="url" rel="canonical">', r.text)
    for link in links:
        print("__________")
        print(root_path+link)
        print("__________")
    #obterNoticias(links, f_descriptor)
