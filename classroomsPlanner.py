from dataReader import get_data
#tab11 i tab#22 -> days like 0,1,2,3,4

class classroomsPlanner:
    def __init__(self, day):
        self.resdata = get_data()
        self.day = day

    def getClassIds(self):  #Pozyskiwanie id gabinetów dla konkretnego dnia (potencjalnie zmienić na wszystkie klasy?)
        classroomIds = list()
        for i in self.resdata['r']['dbiAccessorRes']['tables'][22]['data_rows']:
            if i['day'] == self.day and i['classroomid'] not in classroomIds:
                classroomIds.append(i['classroomid'])
        if not classroomIds:
            return ""
        return classroomIds

    def getClassroomNames(self):    #Pozyskiwanie nazw gabinetów
        classroomNames = list()
        classroomIds = self.getClassIds()
        for i in self.resdata['r']['dbiAccessorRes']['tables'][11]['data_rows']:
            if i['id'] in classroomIds:
                classroomNames.append(i['name'])
        return classroomNames

    def sortClassroomsByHour(self): #Ta metoda nie działa (błędy logiczne) TODO: napisać od nowa (możliwe, że nawet całą klasę)
        classroomNames = self.getClassroomNames()
        print(classroomNames.__len__())
        classroomIds = self.getClassIds()
        print(classroomIds.__len__())
        sortedClassrooms = list()
        for i in range(2,10):
            sortedClassrooms.append(f"Lekcja {i-1}:")
            for j in self.resdata['r']['dbiAccessorRes']['tables'][22]['data_rows']:
                if int(j['break']) == i and j['classroomid'] in classroomIds:
                    sortedClassrooms.append(classroomNames[classroomIds.index(j['classroomid'])])
        return sortedClassrooms
    def createCodeBlockResponse(self, array):   #Formatowanie outputa jako discordowego bloku code w pionowej liście
        response = """```\n{}```""".format("\n".join(array))
        return response
