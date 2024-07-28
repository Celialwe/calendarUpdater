from datetime import datetime, date, time
import icalendar
from pytz import timezone

"""
Create a class to handle the courses
"""
class Heure:
    def __init__(self, h:str):
        """
        h : str est présenté comme suis
        heure_debut - heure_fin
        """
        try :
            heure_debut, heure_fin = h.split(' - ')
            hd = heure_debut.split(':')
            heure_debut = int(hd[0])
            minute_debut = int(hd[1])
            hf = heure_fin.split(':')
            heure_fin = int(hf[0])
            minute_fin = int(hf[1])
            self.startTime = time(heure_debut, minute_debut)
            self.endTime = time(heure_fin, minute_fin)
        except:
            print(h)


class Courses:
    def __init__(self, l : list, cal:icalendar.Calendar, month:int, year:int):
        self.day = int(l[0])
        self.month = month
        self.year = year
        self.cal = cal
        self.l = l[1:]

    def retrieve_course_day(self):
        """
        sépare tous les cours de la journée
        """
        cours = []
        for elem in self.l:
            if len(elem) == 0:
                continue
            if elem[0].isdigit() and len(cours) > 0:
                c = Course(cours, self.cal, self.day, self.month, self.year)
                c.create_event()
                cours = [elem]
            else:
                cours.append(elem)
        if len(cours) > 0:
            c = Course(cours, self.cal, self.day, self.month, self.year)
            c.create_event()
class Course:
    def __init__(self, s:list, cal:icalendar.Calendar,day:int, month:int, year:int):
        """
        s : list est présenté comme suis
        heure, cours, prof, local
        """
        self.s = s
        self.date = date(year, month, day)
        self.local = ''
        for i in range(len(s)):
            match i :
                case 0: 
                    self.heure = Heure(s[i])
                case 1:
                    self.cours = s[i]
                case 2:
                    self.prof = s[i]
                case 3:
                    self.local = s[i]
        self.cal = cal
    #TODO; comprendre pourquoi ça ne marche pas (event tous aglutiné dans un seul jour)
    def create_event(self):
        """
        crée un event avec les informations du cours
        """
        event = icalendar.Event()
        tzone = timezone('Europe/Paris')
        try :
            if self.local == '':
                event.add('summary', self.course)
            else:
                event.add('summary', self.cours + ' - ' + self.local)
            event.add('dtstart', datetime.combine(self.date, self.heure.startTime, tzinfo=tzone))
            event.add('dtend', datetime.combine(self.date, self.heure.endTime, tzinfo=tzone))
            event.add('location', self.local)
            event.add('description', self.cours + ' - ' +self.prof)
            self.cal.add_component(event)
        except:
            print(self.s)
            
        

