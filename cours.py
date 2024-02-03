from datetime import datetime, date, time
import icalendar

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
    def __init__(self, s : str, cal:icalendar.Calendar, month:int, year:int):
        """
        s : str est présenté comme suis
        d
        heure
        cours

        prof

        local
        """
        self.day = int(s[0])
        self.month = month
        self.year = year
        self.cal = cal
        self.s = s

    def retrieve_course_day(self):
        """
        sépare tous les cours de la journée
        """
        s = self.s.split('\n')[1:]
        for i in range(0, len(s), 6):
            c = Course(s[i:i+6], self.cal,self.day, self.month, self.year)
            c.create_event()

class Course:
    def __init__(self, s:list, cal:icalendar.Calendar,day:int, month:int, year:int):
        """
        s : list est présenté comme suis
        heure, cours, \"\", prof, \"\", local
        """
        #s = s.split('\n')
        #print(s)
        self.date = date(year, month, day)
        self.heure = Heure(s[0])
        self.cours = s[1]
        self.prof = s[3]
        self.local = s[5]
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
        
        

