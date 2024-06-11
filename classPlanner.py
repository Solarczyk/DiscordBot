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

    def getGroupIds(self):
        groups = list()
        classId = self.getClassId()
        for i in self.resdata['r']['dbiAccessorRes']['tables'][15]['data_rows']:
            if i['classid'] in classId and i['entireclass'] == False:
                if '1' in i['name'] or '2' in i['name']:
                    groups.append(i['id'])
        return groups
    def getGroupNames(self):
        groups = self.getGroupIds()
        names = list()
        for i in self.resdata['r']['dbiAccessorRes']['tables'][15]['data_rows']:
            if i['id'] in groups:
                if '1' in i['name']:
                    names.append("gr1")
                if '2' in i['name']:
                    names.append("gr2")
        return names
    def getLessonsForSpecificDay(self): #Pozyskiwanie wszystkich lekcji na dany dzień dla podanej klasy
        hours = 0
        hourList = self.getHours()
        subjectNames = self.getSubjectNames()
        day = self.getDayAsNumber()
        groupIds = self.getGroupIds()
        groupNames = self.getGroupNames()
        lessonIds = self.getLessonsIds()

        #Zliczanie godzin lekcyjnych
        for i in self.resdata['r']['dbiAccessorRes']['tables'][20]['data_rows']:
            if i['days'] == day and i['lessonid'] in lessonIds:
                for j in self.resdata['r']['dbiAccessorRes']['tables'][18]['data_rows']:
                    if i['lessonid'] == j['id'] and int(i['period']) > hours:
                        hours = int(i['period']) + int(j['durationperiods'])-1

        #Utworzenie tabeli-szkieletu
        lessonsForTheDay = ['Okienko'] * hours
        for i in self.resdata['r']['dbiAccessorRes']['tables'][20]['data_rows']:
            if i['days'] == day and i['lessonid'] in lessonIds:
                lessonsForTheDay[int(i['period'])-1] = f"({hourList[int(i['period'])-1]}) "+subjectNames[(lessonIds.index((i['lessonid'])))]
                if lessonsForTheDay[int(i['period'])-2] == "Okienko":
                    lessonsForTheDay[int(i['period']) - 2] = f"({hourList[int(i['period'])-2]}) "+lessonsForTheDay[int(i['period'])-2]
                for j in self.resdata['r']['dbiAccessorRes']['tables'][18]['data_rows']:
                    tempGroup = " / "
                    if i['lessonid'] == j['id'] and j['groupids'][0] in groupIds:
                        lessonsForTheDay[int(i['period']) - 1] += f" [{groupNames[groupIds.index(j['groupids'][0])]}]"
                        found = False
                        for z in self.resdata['r']['dbiAccessorRes']['tables'][20]['data_rows']:
                            if z['period'] == i['period'] and z['days'] == i['days']:
                                for x in self.resdata['r']['dbiAccessorRes']['tables'][18]['data_rows']:
                                    if x['id'] == z['lessonid'] and x['groupids'][0] in groupIds and z['lessonid'] in lessonIds and (x['groupids'][0] not in j['groupids'][0] or len(x['groupids']) > 1):
                                        tempGroup += subjectNames[lessonIds.index(z['lessonid'])]
                                        lessonsForTheDay[int(i['period']) - 1] += tempGroup
                                        if 'gr1' in lessonsForTheDay[int(i['period']) - 1]:
                                            lessonsForTheDay[int(i['period']) - 1] += " [gr2]"
                                        else:
                                            lessonsForTheDay[int(i['period']) - 1] += " [gr1]"
                                        found = True
                                        tempGroup = " / "
                                        if x['durationperiods'] > 1:
                                            tempGroup += subjectNames[lessonIds.index(z['lessonid'])]
                                        break  # Przerwij wewnętrzną pętlę
                                if found:
                                    break  # Przerwij zewnętrzną pętlę
                    if i['lessonid'] == j['id'] and j['durationperiods'] > 1:
                        if tempGroup == " / ":
                            for k in range(int(j['durationperiods']) - 1):
                                lessonsForTheDay[int(i['period']) + k] = f"({hourList[int(i['period']) + k]}) " +subjectNames[(lessonIds.index(i['lessonid']))]
                                if j['groupids'][0] in groupIds:
                                    lessonsForTheDay[int(i['period']) + k] += f" [{groupNames[groupIds.index(j['groupids'][0])]}]"
                                    found = False
                                    for z in self.resdata['r']['dbiAccessorRes']['tables'][20]['data_rows']:
                                        if z['period'].isdigit() and int(z['period']) == int(i['period'])+1 and z['days'] == i['days']:
                                            for x in self.resdata['r']['dbiAccessorRes']['tables'][18]['data_rows']:
                                                if x['id'] == z['lessonid'] and x['groupids'][0] in groupIds and z[
                                                    'lessonid'] in lessonIds and (
                                                        x['groupids'][0] not in j['groupids'][0] or len(x['groupids']) > 1):
                                                    tempGroup += subjectNames[lessonIds.index(z['lessonid'])]
                                                    lessonsForTheDay[int(i['period']) + k] += tempGroup
                                                    if 'gr1' in lessonsForTheDay[int(i['period']) - 1]:
                                                        lessonsForTheDay[int(i['period']) + k] += " [gr2]"
                                                    else:
                                                        lessonsForTheDay[int(i['period']) + k] += " [gr1]"
                                                    found = True
                                                    tempGroup = " / "
                                                    break  # Przerwij wewnętrzną pętlę
                                            if found:
                                                break  # Przerwij zewnętrzną pętlę
                        else:
                            for k in range(int(j['durationperiods']) - 1):
                                lessonsForTheDay[int(i['period']) + k] = f"({hourList[int(i['period']) + k]}) " + subjectNames[(lessonIds.index(i['lessonid']))]
                                if j['groupids'][0] in groupIds:
                                    lessonsForTheDay[int(i['period']) + k] += f" [{groupNames[groupIds.index(j['groupids'][0])]}]"
                                    lessonsForTheDay[int(i['period']) + k] += tempGroup
                                    if 'gr1' in lessonsForTheDay[int(i['period']) + k]:
                                        lessonsForTheDay[int(i['period']) + k] += " [gr2]"
                                    else:
                                        lessonsForTheDay[int(i['period']) + k] += " [gr1]"

        return lessonsForTheDay
    def createCodeBlockResponse(self, array):   #Formatowanie outputa jako discordowego bloku code w pionowej liście
        if array == self.getSubjectNames():
            array = list(dict.fromkeys(array))
        response = """```\n{}```""".format("\n".join(array))
        print(response)
        return response
