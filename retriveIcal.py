from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from calendar import monthrange
import icalendar
import time
from cours import Courses
import os



class WebScraping:

    def __init__(self, file = '/Users/celialowagie/Documents/GitHub/calendarUpdater/files/listCourses.json'):
        self.file = file
        self.WAITING_TIME = 4

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

    def extract_courses(self, courses : list,month, year):
        """
        Etant donné une liste de cours, une année et un mois.
        Rajoute tous les cours du mois dans le calendrier défini précédemment
        """
        flag = False
        for course in courses[1:]:
            course = course.text.replace('\n\n', '\n')
            course = course.split('\n')
            #if month == 12:
                #print(course)
            if course[0] == "1":
                    flag = True
            if flag and len(course) > 1 :
                c = Courses(course, self.cal, month, year)
                c.retrieve_course_day()
                if course[0] == str(monthrange(year, month)[1]):
                    flag = False
                    break

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
            EC.presence_of_element_located((By.TAG_NAME,'td'))
        )
        courses = self.browser.find_elements(By.TAG_NAME, 'td')
        month, year = self.get_month_year()
            
        self.extract_courses(courses, month, year)
        

    def next_month(self):
        """
        click sur le bouton pour aller au mois suivant
        """
        next = self.browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[1]/button[2]')
        next.click()
    
    def previous_month(self):
        """
        click sur le bouton pour aller au mois précédent
        """
        prev = self.browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[1]/button[1]')
        prev.click()
    def back_to_september(self):
        """
        click sur le bouton pour aller au mois de septembre
        """
        while self.get_month_year()[0] != 9:
            self.previous_month()
    
    def create_calendar(self):
        """
        crée un calendrier
        """
       
        self.cal = icalendar.Calendar()
        self.cal.add('prodid', '-//My calendar//example.com//')
        self.cal.add('version', '2.0')
        self.get_courses_month()
        while True:
            self.next_month()
            self.get_courses_month()
            if self.get_month_year()[0] == 8:
                break
        with open('files/my.ics', 'wb') as f:
            f.write(self.cal.to_ical())
    
    
    def get_ical(self):
        self.upload_courses()
        self.back_to_september()
        self.create_calendar()
      
        self.browser.close()
        self.browser.quit()
        
        
        
if __name__ == "__main__":
    # Replace these variables with your own values
    
#get_ical()
    web = WebScraping()
    web.get_ical()
#test ical



