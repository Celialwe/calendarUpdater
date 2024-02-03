from datetime import datetime, date, time
import icalendar

class Heure:
    def __init__(self, h:str):
        """
        h : str est présenté comme suis
        heure_debut - heure_fin
        """
        
        heure_debut, heure_fin = h.split(' - ')
        heure_debut = int(heure_debut.split(':')[0])
        minute_debut = int(heure_debut.split(':')[1])
        heure_fin = int(heure_fin.split(':')[0])
        minute_fin = int(heure_fin.split(':')[1])
        self.startTime = time(heure_debut, minute_debut)
        self.endTime = time(heure_fin, minute_fin)
class Course:
    def __init__(self, s:str, cal:icalendar.Calendar, month:int, year:int):
        """
        s : str est présenté comme suis
        d
        heure
        cours

        prof

        local
        """
        s = s.split('\n')
        self.date = date(year, month, int(s[0]))
        self.heure = Heure(s[1])
        self.cours = s[2]
        self.prof = s[4]
        self.local = s[6]
        self.cal = cal
    
    def create_event(self):
        """
        crée un event avec les informations du cours
        """
        event = icalendar.Event()
        event.add('summary', self.cours)
        event.add('dtstart', datetime.combine(self.date, self.heure.startTime))
        event.add('dtend', datetime.combine(self.date, self.heure.endTime))
        event.add('location', self.local)
        event.add('description', self.cours + ' - ' +self.prof)
        self.cal.add_component(event)
        
        

