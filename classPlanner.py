import json
from dataReader import get_data

class classPlanner:
    def __init__(self, name, day):
        self.name = name
        self.resdata = get_data()
        self.day = day

    def getClassId(self):
        className = self.name[:1] + self.name[1].upper() + self.name[2:]
        classId = ''
        for i in self.resdata['r']['dbiAccessorRes']['tables'][12]['data_rows']:
            if className in i['name']:
                classId = i['id']
                break
        return classId

    def getDayAsNumber(self):
        if self.day == 'poniedzialek' or self.day == 'poniedziałek':
            return "10000"
        elif self.day == 'wtorek':
            return "01000"
        elif self.day == 'środa' or self.day == "sroda":
            return "00100"
        elif self.day == 'czwartek':
            return "00010"
        elif self.day == 'piątek' or self.day == "piatek":
            return "00001"
        else:
            return ""

    def getLessonsIds(self):
        lessonIds = list()
        classId = self.getClassId()
        for i in self.resdata['r']['dbiAccessorRes']['tables'][18]['data_rows']:
            if classId in i['classids']:
                lessonIds.append(i['id'])
        return lessonIds

    def getSubjectNames(self):
        lessonIds = self.getLessonsIds()
        subjectNames = list()
        for i in self.resdata['r']['dbiAccessorRes']['tables'][18]['data_rows']:
            if i['id'] in lessonIds:
                for j in self.resdata['r']['dbiAccessorRes']['tables'][13]['data_rows']:
                    if j['id'] == i['subjectid']:
                        subjectNames.append(j['name'])
                        break
        return subjectNames

    def getLessonsForSpecificDay(self): #TODO - Indexy tabeli nie działają przy każdym dniu
        hours = 1
        day = self.getDayAsNumber()
        lessonIds = self.getLessonsIds()
        for i in self.resdata['r']['dbiAccessorRes']['tables'][20]['data_rows']:
            if i['days'] == day and i['lessonid'] in lessonIds:
                hours += 1
        lessonsForTheDay = ['None'] * hours
        for i in self.resdata['r']['dbiAccessorRes']['tables'][20]['data_rows']:
            if i['days'] == day and i['lessonid'] in lessonIds:
                lessonsForTheDay[int(i['period'])] = self.getSubjectNames()[(lessonIds.index(i['lessonid']))]
                for j in self.resdata['r']['dbiAccessorRes']['tables'][18]['data_rows']:
                    if i['lessonid'] == j['id'] and j['durationperiods'] > 1:
                        lessonsForTheDay[int(i['period'])+1] = self.getSubjectNames()[(lessonIds.index(i['lessonid']))]
        return lessonsForTheDay
    def createCodeBlockResponse(self, array):
        response = """```{}```""".format("\n".join(array))
        return response
