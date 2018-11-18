import re

def cssSelector(texto, css_pattern):
	selectors=css_pattern.split(' ')
	for selector in selectors:
		if selector[0] == '.':
			texto = find_class(texto, selector[1:])
		elif selector[0] == '#':
			texto = find_id(texto, selector[1:])
		else:
			texto = find_element(texto, selector)
	return texto

# TODO: refine search to capture the whole tag
def find_class(texto, html_class):
	return re.findall(r'<[^>]*class=\"'+html_class+r'\"[^>]*>', texto)


def find_id(texto, html_id):
	return re.findall(r'<[^>]*id=\"'+html_id+r'\"[^>]*>', texto)

def find_element(texto, html_element):
	return re.findall(r'<'+html_element+r'[^>]*><\/'+html_element+r'[^>]*>', texto)