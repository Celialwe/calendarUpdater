from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import icalendar
import time
from cours import Course

WAITING_TIME = 2

class WebScraping:

    def __init__(self, file = '/Users/celialowagie/Documents/GitHub/calendarUpdater/listCourses.json'):
        self.file = file
        self.WAITING_TIME = 2
        self.get_ical()

    def upload_courses(self):
        """
        upload le fichier json contenant les cours et met l'horaire en mode mois
        """
        self.browser = webdriver.Firefox()
        self.browser.maximize_window()
        url = "https://shinkumons.github.io/NovaPlanning/config.html"
        self.browser.get(url)

        #envoyer le fichier 
        elem = self.browser.find_element(By.XPATH, '//*[@id="myFile"]')
        elem.send_keys(self.file)
        #click sur upload pour upload le fichier qui a été envoyé
        upload = self.browser.find_element(By.XPATH, '/html/body/button[2]')
        upload.click()
        #click sur le bouton pour retourner à la page d'accueil
        backToHome = self.browser.find_element(By.XPATH, '/html/body/a/button')
        backToHome.click()
    
        WebDriverWait(self.browser,self.WAITING_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME,'fc-button-group'))
        )
        #changer la vision en mois
        month = self.browser.find_elements(By.CLASS_NAME,'fc-button-group')
        for e in month:
            #print(e.text)
            if "month" in e.text:
                e.click()
                break

    def get_month_year(self):
        """
        retourne le mois et l'année actuelle sur la page
        """
        month = self.browser.find_element(By.ID, 'fc-dom-1')
        dico = {"Janvier":1, "Février":2, "Mars":3, "Avril":4, "Mai":5, "Juin":6, "Juillet":7, "Août":8, "Septembre":9, "Octobre":10, "Novembre":11, "Décembre":12}
        s = month.text.split(' ')
        month = dico[s[0]]
        year = int(s[1])
        return month, year

    def extract_courses(self, courses : list,month, year, fromStart = True):
        """
        Etant donné une liste de cours, une année et un mois.
        Rajoute tous les cours du mois dans le calendrier défini précédemment
        """
        flag = False
        for course in courses:
            if fromStart:
                if course.text[1] == "1":
                    flag = True
            elif not fromStart:
                if course.text[1] == datetime.now().day:
                    flag = True
            elif flag:
                if course.text[1] == datetime.monthrange(year, month)[1]:
                    break
            if flag and len(course.text) > 1:
                c = Course(course.text, self.cal, month, year)
                c.create_event()

    def get_courses_month(self):
        #présenté comme suis
        """
        d
        heure
        cours

        prof

        local
        """
        WebDriverWait(self.browser,self.WAITING_TIME).until(
            EC.presence_of_element_located((By.TAG_NAME, 'td'))
        )
        courses = self.browser.find_elements(By.TAG_NAME, 'td')
        month, year = self.get_month_year()
        if datetime.now().month == month:
            self.extract_courses(courses, month, year, False)
        else:
            self.extract_courses(courses, month, year)
           

        

    def next_month(self):
        """
        click sur le bouton pour aller au mois suivant
        """
        next = self.browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[1]/button[2]')
        next.click()
    

    def get_ical(self):
        self.upload_courses()

        self.cal = icalendar.Calendar()
        self.cal.add('prodid', '-//My calendar//example.com//')
        self.cal.add('version', '2.0')
        self.get_courses_month()
        while True:
            self.next_month()
            self.get_courses_month()
            if self.get_month_year()[0] == 8:
                break

        #days = self.browser.find_elements(By.CLASS_NAME, 'fc-daygrid-day-top')
        
        
        

#get_ical()
web = WebScraping()

#test ical


