import requests
import re
import sys
import html

def limparParagrafo(paragrafo):
	return html.unescape(paragrafo)

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
		print(description[0] + '\n')
		for image in images:
			print(image)
		for paragrafo in paragrafos:
			print(limparParagrafo(paragrafo))
		print("\n---------------------------------\n")

def pesquisarNoticias():
	for argument in sys.argv[1:]:
		print("Termo de pesquisa: " + argument)
		
		payload = {'query':argument}
		
		r = requests.get('https://www.publico.pt/pesquisa', params = payload)
		print('URL = ' + r.url)

		links = re.findall(r'<div class="media-object-section">\s*<a href="(.*)">', r.text)
		#print(links)

		obterNoticias(links)

pesquisarNoticias()