from tkinter import *
from pandastable import Table, TableModel
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import tkinter as tk




class TestApp(Frame):
    """Basic test frame for the table"""
    def __init__(self, parent=None):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        frame1 = Frame(self.main)
        self.main.geometry('800x500+200+100')

        self.sv = Entry(frame1)
        self.sv.grid(row=0, column=0)
        self.Btn = Button(frame1, text="Search", command=self.scrapIt)
        self.Btn.grid(row=0,column=1)

        frame1.pack()

        self.main.title('Table app')
        f = Frame(self.main)
        f.pack(fill=BOTH, expand=1)

        self.table = Table(f,showtoolbar=False, showstatusbar=True)
        #self.table.importCSV('data.csv')
        self.table.show()
        self.main.mainloop()
        return

    def scrapIt(self):
        url = f"https://www.ouedkniss.com/{self.sv.get()}-r"
        #url = f"https://www.ouedkniss.com/ps4-r"
        r = requests.get(url)
        #print(r.content)
        '<h2 itemprop="name"><h2>'
        soup = bs(r.content, 'html5lib')

        #print(soup.prettify())

        table = soup.findAll('div')  # ,atttr={"id":"page"})
        #print(len(table))
        x = 0
        res = []
        for d in table:
            try:
                #print("id",x,d['id'])
                pass
            except:
                pass
            try:
                #print("class",x,d['class'],type(d['class']))
                if "annonce" in d['class']:
                    res.append(d)
            except:
                pass
            x += 1
            #,d['class'])
        links = []
        noms = []  # <div class="annonce_right">
        titres = []  # <div class="annonce_buttons">
        wilayas = []  # <p class="annonce_wilaya">
        #print(res[0].prettify())
        for resu in res:
            x = 0
            for di in resu.findAll('div'):
                if x == 0:
                    try:
                        #print('wilaya : ', str(di.find('p')).split('<span class="titre_wilaya">')[1].split('</span>')[0])
                        wilayas.append(str(di.find('p')).split(
                            '<span class="titre_wilaya">')[1].split('</span>')[0])
                    except:
                        pass
                        #print('no wilaya')
                elif x == 2:
                    try:
                        nom = di.findAll('a')[3]
                        #print('nom :', nom['href'].split('"')[1].split('"')[0])
                        noms.append(nom['href'].split('"')[1].split('"')[0])
                    except:
                        pass
                        #print('no name')
                    try:
                        data = di.findAll('a')[1]
                        titres.append(data['title'])
                        url = "https://www.ouedkniss.com/"+data['href']
                        soup2 = (requests.get(url).content)
                        nums = str(soup2).split('tel:')[1].split("\\'>")[0]
                        links.append(nums)
                        #print('titre ', titres)
                        #print('num ', nums)
                    except:
                        print('no data')
                else:
                    pass
                x += 1
            print('--------------')
        df = pd.DataFrame(list(zip(noms, titres, wilayas, links)),
                        columns=['NOM', 'Titre', 'Wilaya', 'NUM'])
        df = df.drop_duplicates(subset=["NOM", "NUM"])
        df.to_csv(f"{self.sv.get()}.csv", index=False)
        #print(dir(self.table))
        self.table.importCSV(f"{self.sv.get()}.csv")
        
TestApp()

