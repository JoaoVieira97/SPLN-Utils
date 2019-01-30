#!/usr/bin/env python3
from tkinter import *
import os, webbrowser
import regex as re
import rsspider

class Application:
    def __init__(self, master=None):
        self.results = []
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
        self.search.pack()

        self.msg_search = Label(self.terceiroContainer, text="", font=("Arial", "12"))
        self.msg_search.pack(side=BOTTOM)

        # --------------------------------------------

        self.quartoContainer = Frame(master)
        self.quartoContainer["padx"] = 20
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()
        
        self.results_label = Label(self.quartoContainer,text="Search Results", font=("Calibri", "18", "bold"))
        self.results_label.pack()

    def refreshFeed(self):
        rsspider.refreshDB()
        self.mensagem_refresh["text"] = "Feed refresh done!"

    def searchQuery(self):
        for prev_res in self.quartoContainer.winfo_children():
            if isinstance(prev_res, Button):
                prev_res.destroy()
        query = self.query_string.get()
        query = re.sub(r'\p{punct}', r'', query)
        query = list(filter(lambda x: len(x)>0, re.split(r'\s+', query)))       #remove empty query terms
        if len(query)==0:
            self.msg_search["text"] = "Bad query for the search. Try again!"
        else:
            self.results = rsspider.procRequest(query)
            self.msg_search["text"] = "Search done. Look for your results!"
            for result in self.results:
                resfield = Button(self.quartoContainer, text=result, command= lambda : self.openDocument(rsspider.directory+result))
                resfield.pack()
    
    def openDocument(self, filename):
        webbrowser.open('file://' + os.path.realpath(filename))

root = Tk()
root.title("RSSpider")
root.update_idletasks()
Application(root)
root.mainloop()