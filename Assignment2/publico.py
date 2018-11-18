import requests
import re
import sys
import html
from urllib.request import urlretrieve

file = open("noticias.tex", "w")
img_nb = 1

def limparTexto(texto):
	t = re.sub(r'<a href=".*".*>(.*)</a>', r'\1', texto)
	t = re.sub(r'<.*>', ' ', t)
	return html.unescape(t)

def obterNoticias(links):
	for link in links:
		print('Link = ' + link + '\n')

		link_content = requests.get(link)
		titulo = re.findall(r'<title>(.*)\s*.*</title>', link_content.text)
		description = re.findall(r'<div class="story__blurb lead" itemprop="description">\s*<p>(.*)</p>\s*</div>', link_content.text)
		images = re.findall(r'data-media-viewer="(.*)"', link_content.text)

		paragrafos = re.findall(r'<div class="story__body" id="story-body">\s*<p>(.*)\s*</p>', link_content.text)
		paragrafos = paragrafos + re.findall(r'<p>\s*(.*)\s*</p>.*\s*.*<aside class=".*">', link_content.text)

		print(titulo[0] + '\n')
		print(limparTexto(description[0]) + '\n')
		for image in images:
			print(image)
		for paragrafo in paragrafos:
			print(limparTexto(paragrafo))
		print("\n---------------------------------\n")
		escreverLatex(titulo[0], description[0], images, paragrafos)

def iniciarLatex():
	file.write("\\documentclass{article}\n")
	file.write("\\usepackage[a4paper, top=3cm, left=3cm, right=2.5cm, bottom=2.5cm]{geometry}\n")
	file.write("\\usepackage[utf8]{inputenc}\n")
	file.write("\\usepackage{graphicx}\n\n")
	file.write("\\begin{document}\n\n")

def escreverLatex(titulo, description, images, paragrafos):
	file.write("\\section{" + titulo + "}\n\n")
	file.write("\\textbf{" + description + "}\n\n")
	#for image in images:
		#GUARDAR IMAGEM E SEU PATH, ESCREVER NO LATEX
	for paragrafo in paragrafos:
		file.write(limparTexto(paragrafo))

def pesquisarNoticias():
	for argument in sys.argv[1:]:
		print("Termo de pesquisa: " + argument)
		payload = {'query':argument}
		r = requests.get('https://www.publico.pt/pesquisa', params = payload)
		print('URL = ' + r.url)
		links = re.findall(r'<div class="media-object-section">\s*<a href="(.*)">', r.text)
		#print(links)
		obterNoticias(links)

iniciarLatex()
pesquisarNoticias()
file.write("\n\n\\end{document}\n")