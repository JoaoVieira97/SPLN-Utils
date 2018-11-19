import requests
import re
import sys
import os
import html
import latex_utils
from urllib.request import urlretrieve
from unidecode import unidecode

def obterNoticias(links, out):
    for link in links:
        print('Link = ' + link + '\n')

        link_content = requests.get(link)
        titulo = re.findall(r'<title>(.*[^\s\n\t\r])\s+\|.*\| PÚBLICO</title>', link_content.text)
        description = re.findall(r'<div class="story__blurb lead" itemprop="description">\s*<p>(.*)</p>\s*</div>', link_content.text)
        images = re.findall(r'data-media-viewer="(.*)"', link_content.text)

        paragrafos = re.findall(r'<div class="story__body" id="story-body">\s*<p>(.*)\s*</p>', link_content.text)
        paragrafos = paragrafos + re.findall(r'<p>\s*(.*)\s*</p>.*\s*.*<aside class=".*">', link_content.text)

        
        tex_folder = ".files/" + ''.join(unidecode(titulo[0]).split(' ')).lower()
        tex_folder = re.sub(r'"',r'',tex_folder)
        os.makedirs(tex_folder, exist_ok=True)

        print(titulo[0] + '\n')
        print(latex_utils.limparTexto(description[0]) + '\n')
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

        for paragrafo in paragrafos:
            print(latex_utils.limparTexto(paragrafo))
        print("\n---------------------------------\n")
        latex_utils.escreverLatex(out, titulo[0], description[0], img_paths, paragrafos)


def pesquisarNoticias(argument, f_descriptor):
    print("Termo de pesquisa: " + argument)
    payload = {'query':argument}
    r = requests.get('https://www.publico.pt/pesquisa', params = payload)
    print('URL = ' + r.url)
    links = re.findall(r'<div class="media-object-section">\s*<a href="(.*)">', r.text)
    #print(links)
    obterNoticias(links, f_descriptor)

def main():
    for argument in sys.argv[1:]:
        f_descriptor = open("noticias_"+argument+".tex", "w")
        latex_utils.iniciarLatex(f_descriptor)
        pesquisarNoticias(argument, f_descriptor)
        f_descriptor.write("\n\\end{document}")
        f_descriptor.close()

if __name__=="__main__":
    main()
