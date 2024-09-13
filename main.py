#!/Users/celialowagie/miniconda3/envs/calendarUpdater/bin/python

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title updateHoraire
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 🤖

# Documentation:
# @raycast.description update the calendar

import os

import icalendar
from retriveIcal import WebScraping
import dropbox
from dropbox.exceptions import AuthError
import requests
from selenium import webdriver
from time import sleep

filePath = os.path.join(os.getcwd(), "files") 
class Main:
    
    def __init__(self, local, dropbox):
        self.localPath = local
        self.dropboxPath = dropbox
        with open(os.path.join(filePath,"appCredentials.txt"), 'r') as file:
            self.AppKey = file.readline().strip()
            self.AppSecret = file.readline().strip()
        with open(os.path.join(filePath, 'token.txt'), 'r') as file:
            self.access_token = file.read()
            if len(self.access_token) == 0:
                self.get_access_token()
    
    def get_dropbox_access_token(self):
        # Get the access token from the user
        print("Please enter your Dropbox access token.")
        print("Don't have one? You can generate one here: https://www.dropbox.com/developers/documentation/http/overview")
        self.access_token = input("Access token: ")
        with open(os.path.join(filePath, 'token.txt'), 'w') as file:
            file.write(self.access_token)
    
    def get_access_token(self):
        authorize_url = "https://www.dropbox.com/oauth2/authorize?client_id=vhgy00ak8ap02dj&response_type=code&token_access_type=offline&redirect_uri=https://localhost"
        print("1. Go to: " + authorize_url)
        auth_code = input("Enter the authorization code here: ").strip()
        data = {
            "code": auth_code,
            "grant_type": "authorization_code",
            "client_id": self.AppKey,
            "client_secret": self.AppSecret,
            "redirect_uri": "https://localhost"
        }
        response = requests.post("https://api.dropboxapi.com/oauth2/token", data=data)
        access_token = response.json()["access_token"]
        refresh_token = response.json()["refresh_token"]
        with open(os.path.join(filePath,'refresh_token.txt'), 'w') as file:
            file.write(refresh_token)
        with open(os.path.join(filePath,'token.txt'), 'w') as file:
            file.write(access_token)
        self.access_token = access_token
    
    def refresh_access_token(self):
        with open(os.path.join(filePath,'refresh_token.txt'), 'r') as file:
            refresh_token = file.read()
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.AppKey,
            "client_secret": self.AppSecret
        }
        response = requests.post("https://api.dropboxapi.com/oauth2/token", data=data)
        access_token = response.json()["access_token"]
        with open(os.path.join(filePath,'token.txt'), 'w') as file:
            file.write(access_token)
        self.access_token = access_token

    def chatgpyMethod(self):
        auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(self.AppKey, self.AppSecret)
        authorize_url = auth_flow.start()
        print("1. Go to: " + authorize_url)
        auth_code = input("Enter the authorization code here: ").strip()
        access_token = auth_flow.finish(auth_code)
        return access_token

    #TODO regler le probleme de l'access token
    def upload_to_dropbox(self):
        try:
            # Connect to Dropbox using the access token
            dbx = dropbox.Dropbox(self.access_token)
            
            # Upload the file
            with open(self.localPath, 'rb') as f:
                dbx.files_upload(f.read(), self.dropboxPath, mode=dropbox.files.WriteMode('overwrite'))

            print("File uploaded successfully.")
        except AuthError as e:
            with open(os.path.join(filePath,'refresh_token.txt'), 'r') as file:
                refresh = file.read()
                if len(refresh)  == 0:
                    self.get_access_token()
                else:
                    self.refresh_access_token()
            #refresh = chatgpyMethod()
            self.upload_to_dropbox()
        except Exception as e:
            print(f"Error uploading file: {e}")

def create_ical(filename : str):
    cal = icalendar.Calendar()
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')
    fpath = os.path.join(filePath,"listeCalend", f'{filename}.ics')
    with open(fpath, 'wb') as f:
        f.write(cal.to_ical())

if __name__ == "__main__":
    # Replace these variables with your own values
    for listcours in os.listdir(os.path.join(filePath,"listeCours")):
        
        if listcours == '.DS_Store':
            continue
        nom = listcours.split('.')[0]
        calendarDoc = os.path.join(filePath,'listeCalend')
        if len(os.listdir(calendarDoc)) < len(nom):
            #TODO faire en sorte que ça marche même si le calendrier n'est pas là
            for i in range(len(os.listdir(calendarDoc)),len(nom)):
                create_ical(nom)
        
        
        updater = WebScraping(os.path.join(filePath,"listeCours", listcours), os.path.join(filePath, 'listeCalend', f'{nom}.ics'))
        updater.get_ical(nom)

        local_file_path = os.path.join(filePath, 'listeCalend', f'{nom}.ics')
        dropbox_path = f'{os.sep}{nom}.ics'
    
        m = Main(local_file_path, dropbox_path)
        m.upload_to_dropbox()
