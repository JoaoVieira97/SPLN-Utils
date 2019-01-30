from tkinter import *
import os
  
class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "20")

        # --------------------------------------------

        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="RSSpider")
        self.titulo["font"] = ("Comic Sans", "16", "bold")
        self.titulo.pack()

        # --------------------------------------------

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.refresh = Button(self.segundoContainer, text = "Refresh", font = ("Calibri", "20"), fg = "black", command = self.refreshFeed)
        self.refresh["width"] = 20
        self.refresh.pack()

        self.mensagem_refresh = Label(self.segundoContainer, text="", font=("Arial", "12"))
        self.mensagem_refresh.pack()

        # --------------------------------------------

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer["pady"] = 20
        self.terceiroContainer.pack()

        self.query = Label(self.terceiroContainer,text="Search Query", font=("Calibri", "15"))
        self.query.pack(side=LEFT)
  
        self.query_string = Entry(self.terceiroContainer)
        self.query_string["width"] = 40
        self.query_string["font"] = ("Calibri", "15")
        self.query_string.pack(side=LEFT)

        self.search = Button(self.terceiroContainer, text = "Search", font = ("Calibri", "15"), fg = "black", command = self.searchQuery)
        self.search["width"] = 20
        self.search.pack(side=RIGHT)

        self.mensagem_search = Label(self.terceiroContainer, text="", font=("Arial", "12"))
        self.mensagem_search.pack(side=BOTTOM)

    def refreshFeed(self):
        cmd = 'python3 rsspider.py -r'
        os.system(cmd)
        self.mensagem_refresh["text"] = "Feed refresh done!"

    def searchQuery(self):
        query = self.query_string.get()
        if query == r'\s+':
            self.mensagem_search["text"] = "Bad query for the search. Try again!"
        else:
            cmd = 'python3 rsspider.py -s ' + query
            os.system(cmd)
            self.mensagem_search["text"] = "Search done. Look for your results!"

root = Tk()
root.title("RSSpider")
Application(root)
root.mainloop()