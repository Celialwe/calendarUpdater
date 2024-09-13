from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from calendar import monthrange
import icalendar
import time
from pytz import timezone
from cours import Courses
import os


filePath = os.path.join(os.getcwd(), "files") 
class WebScraping:

    def __init__(self, file = os.path.join(os.getcwd(), "listCourses.json"), calendrier = ''):
        self.file = file
        with open(calendrier, 'rb') as f:
            self.calendrier = icalendar.Calendar.from_ical(f.read())
         
        self.WAITING_TIME = 4

    def  upload_courses(self):
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
        dico = {"janvier":1, "février":2, "mars":3, "avril":4, "mai":5, "juin":6, "juillet":7, "août":8, "septembre":9, "octobre":10, "novembre":11, "décembre":12}
        s = month.text.split(' ')
        month = dico[s[0].lower()]
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
    
    
    def delete_events_after_date(self):
        """
        create calendar with events that have already passed
        """
        currentDate = datetime.now()
        cutoff_date = datetime(currentDate.year,currentDate.month, 1, tzinfo= timezone("Europe/Brussels"))
        events_to_keep = []
        for component in self.calendrier.walk():
            if component.name == "VEVENT":
                event_date = component.get('DTSTART').dt
                if event_date < cutoff_date:
                    events_to_keep.append(component)
        # Créer un nouveau calendrier avec les événements restants
        self.cal = icalendar.Calendar()
        self.cal.add('prodid', '-//My calendar//example.com//')
        self.cal.add('version', '2.0')
        for event in events_to_keep:
            self.cal.add_component(event)

    def create_calendar(self, nom : str):
        """
        crée un calendrier
        """

        self.delete_events_after_date()
        self.get_courses_month()
        while True:
            self.next_month()
            self.get_courses_month()
            if self.get_month_year()[0] == 8:
                break
        with open(os.path.join(filePath, 'listeCalend', f'{nom}.ics'), 'wb') as f:
            f.write(self.cal.to_ical())
    
    
    def get_ical(self, nom : str):
        self.upload_courses()
        self.create_calendar(nom)
      
        self.browser.close()
        self.browser.quit()
        

        
if __name__ == "__main__":
    # Replace these variables with your own values
    for listcours in os.listdir("/Users/celialowagie/Documents/GitHub/calendarUpdater/files/listeCours"):

        web = WebScraping(f'/Users/celialowagie/Documents/GitHub/calendarUpdater/files/listeCours/{listcours}')
        web.get_ical(listcours.split('.')[0])




