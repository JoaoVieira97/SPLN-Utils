def iniciarLatex(f_descriptor):
    f_descriptor.write("\\documentclass{article}\n")
    f_descriptor.write("\\usepackage[a4paper, top=3cm, left=3cm, right=2.5cm, bottom=2.5cm]{geometry}\n")
    f_descriptor.write("\\usepackage[utf8]{inputenc}\n")
    f_descriptor.write("\\usepackage{graphicx}\n")
    f_descriptor.write("\\usepackage{float}\n")
    f_descriptor.write("\\begin{document}\n\n")

def escreverLatex(out, titulo, description, images, paragrafos):
    out.write("\\section{" + titulo + "}\n\n")
    out.write("\\textbf{" + description + "}\n\n")
    for image in images:
       adicionar_img(out, image) 
    for paragrafo in paragrafos:
        out.write(paragrafo)

def adicionar_img(out, img_path):
    out.write('\\begin{figure}[H]\n')
    out.write('\t\\centering\n')
    out.write('\t\\includegraphics{'+img_path+'}\n')
    out.write('\\end{figure}')
