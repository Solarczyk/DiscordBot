import json
from dataReader import get_data

class classPlanner:
    def __init__(self, name, day):
        self.name = name
        self.resdata = get_data()
        self.day = day

    def getClassId(self): #Pozyskiwanie id klasy
        className = self.name[:1] + self.name[1].upper() + self.name[2:]
        classId = ''
        for i in self.resdata['r']['dbiAccessorRes']['tables'][12]['data_rows']:
            if className in i['name']:
                classId = i['id']
                break
        return classId

    def getDayAsNumber(self):
        print(self.day)
        if self.day == "poniedziałek":
            return "10000"
        elif self.day == 'wtorek':
            return "01000"
        elif self.day == 'środa':
            return "00100"
        elif self.day == 'czwartek':
            return "00010"
        elif self.day == 'piątek':
            return "00001"
        else:
            return ""

    def getLessonsIds(self):    #Pozyskiwanie id lekcji (nie przedmiotu)
        lessonIds = list()
        classId = self.getClassId()
        for i in self.resdata['r']['dbiAccessorRes']['tables'][18]['data_rows']:
            if classId in i['classids']:
                lessonIds.append(i['id'])
        return lessonIds

    def getSubjectNames(self):  #Pozyskiwanie nazw przedmiotów
        lessonIds = self.getLessonsIds()
        subjectNames = list()
        for i in self.resdata['r']['dbiAccessorRes']['tables'][18]['data_rows']:
            if i['id'] in lessonIds:
                for j in self.resdata['r']['dbiAccessorRes']['tables'][13]['data_rows']:
                    if j['id'] == i['subjectid']:
                        subjectNames.append(j['name'])
                        break
        return subjectNames
    def getHours(self):
        hours = list()
        for i in self.resdata['r']['dbiAccessorRes']['tables'][1]['data_rows']:
            hours.append(i['starttime']+" - "+i['endtime'])
        return hours
    def getLessonsForSpecificDay(self): #Pozyskiwanie wszystkich lekcji na dany dzień dla podanej klasy
        hours = 0
        hourList = self.getHours()
        day = self.getDayAsNumber()
        lessonIds = self.getLessonsIds()
        for i in self.resdata['r']['dbiAccessorRes']['tables'][20]['data_rows']:
            if i['days'] == day and i['lessonid'] in lessonIds:
                for j in self.resdata['r']['dbiAccessorRes']['tables'][18]['data_rows']:
                    if i['lessonid'] == j['id'] and int(i['period']) > hours:
                        hours = int(i['period']) + int(j['durationperiods'])-1
        lessonsForTheDay = ['Okienko'] * hours
        for i in self.resdata['r']['dbiAccessorRes']['tables'][20]['data_rows']:
            if i['days'] == day and i['lessonid'] in lessonIds:
                lessonsForTheDay[int(i['period'])-1] = f"({hourList[int(i['period'])-1]}) "+self.getSubjectNames()[(lessonIds.index((i['lessonid'])))]
                if lessonsForTheDay[int(i['period'])-2] == "Okienko":
                    lessonsForTheDay[int(i['period']) - 2] = f"({hourList[int(i['period'])-2]}) "+lessonsForTheDay[int(i['period'])-2]
                for j in self.resdata['r']['dbiAccessorRes']['tables'][18]['data_rows']:
                    if i['lessonid'] == j['id'] and j['durationperiods'] > 1:
                        lessonsForTheDay[int(i['period'])] = f"({hourList[int(i['period'])]}) "+self.getSubjectNames()[(lessonIds.index(i['lessonid']))]
        return lessonsForTheDay
        # TODO - Wyświetlić w tej samej linii lekcje podzielone na grupy (/)
    def createCodeBlockResponse(self, array):   #Formatowanie outputa jako discordowego bloku code w pionowej liście
        if array == self.getSubjectNames():
            array = list(dict.fromkeys(array))
        response = """```\n{}```""".format("\n".join(array))
        print(response)
        return response
