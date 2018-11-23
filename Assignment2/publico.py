import requests
import re
import sys
import os
import html
import latex_utils
from urllib.request import urlretrieve
from unidecode import unidecode

def obterNoticias(links, out):
    errors_output = open("errors_output.txt", "w")
    for link in links:
        print('A processar ' + link + ' ... ')

        link_content = requests.get(link)
        titulo = re.findall(r'<title>(.*[^\s\n\t\r])\s+\|.*\| PÚBLICO</title>', link_content.text)
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
        print("Imprimido no documento!\n---------------------------------")
        latex_utils.escreverLatex(out, titulo[0], description, img_paths, paragrafos)


def pesquisarNoticias(argument, f_descriptor):
    print("Termo de pesquisa: " + argument)
    payload = {'query':argument}
    r = requests.get('https://www.publico.pt/pesquisa', params = payload)
    print('URL de pesquisa = ' + r.url + '\n')
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
        os.system("pdflatex noticias_" + argument + ".tex > /dev/null")
        os.system("evince noticias_" + argument + ".pdf")

if __name__=="__main__":
    main()
