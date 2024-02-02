from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Firefox()

def upload_courses(file = '/Users/celialowagie/Documents/GitHub/calendarUpdater/listCourses.json'):
    url = "https://shinkumons.github.io/NovaPlanning/config.html"
    browser.get(url)

    #envoyer le fichier 
    elem = browser.find_element(By.XPATH, '//*[@id="myFile"]')
    elem.send_keys(file)
    #click sur upload pour upload le fichier qui a été envoyé
    upload = browser.find_element(By.XPATH, '/html/body/button[2]')
    upload.click()
    #click sur le bouton pour retourner à la page d'accueil
    backToHome = browser.find_element(By.XPATH, '/html/body/a/button')
    backToHome.click()
    
    #changer la vision en mois
    #month = browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[2]/button[2]')
    #month.click()
    next = browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[1]/button[2]/span')
    next.click()

def get_ical():
    upload_courses()
    
    courses = browser.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div/table/tbody/tr[2]/td/div/div/div/div[2]/table/tbody/tr/td[2]/div/div[2]/div[2]/a/div/div/div[2]/div')
    print(courses)

get_ical()