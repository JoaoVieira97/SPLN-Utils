import re
import html

def iniciarLatex(f_descriptor):
    f_descriptor.write("\\documentclass{article}\n")
    f_descriptor.write("\\usepackage[a4paper, top=3cm, left=3cm, right=2.5cm, bottom=2.5cm]{geometry}\n")
    f_descriptor.write("\\usepackage[utf8]{inputenc}\n")
    f_descriptor.write("\\usepackage{graphicx}\n")
    f_descriptor.write("\\usepackage{float}\n")
    f_descriptor.write("\\usepackage{eurosym}\n")
    f_descriptor.write("\\begin{document}\n\n")

def escreverLatex(out, titulo, description, images, paragrafos):
    out.write("\\section{" + limparTexto(titulo) + "}\n\n")
    if description:
        out.write("\\textbf{" + limparTexto(description[0]) + "}\n\n")
    for image in images:
       adicionar_img(out, image) 
    for paragrafo in paragrafos:
        if (paragrafo != "Subscreva gratuitamente as newsletters e receba o melhor da actualidade e os trabalhos mais profundos do Público."):
            out.write(limparTexto(paragrafo) + "\\newline\n")
    out.write("\n\\newpage\n")

def adicionar_img(out, img_path):
    out.write('\\begin{figure}[H]\n')
    out.write('\t\\centering\n')
    out.write('\t\\includegraphics[width=0.3\\textwidth]{'+img_path+'}\n')
    out.write('\\end{figure}\n\n')

def limparTexto(texto):
    t = html.unescape(texto)
    t = re.sub(r'<h2><strong>([^<]*)</strong></h2>', r'\\subsection{\1}\n\n', t)
    t = re.sub(r'<a[^>]*>([^<]*)</a>', r'\1', t)
    t = re.sub(r'<i>([^<]*)</i>', r'\\textit{\1}', t)
    t = re.sub(r'<strong>([^<]*)</strong>', r'\\textbf{\1}', t)
    t = re.sub(r'<[^<]*>', r'', t)
    t = re.sub(r'([#$%&])', r'\\\1', t)
    t = re.sub(r'€', r'\\euro', t)
    return t
