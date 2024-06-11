from dataReader import get_data
#tab11 i tab#22 -> days like 0,1,2,3,4

class classroomsPlanner:
    def __init__(self, day, hour, building):
        self.resdata = get_data()
        self.day = day
        self.hour = str(hour)
        self.building = building

    def getBuildingId(self):
        if self.building == "główny" or self.building == "glowny" or self.building == "main":
            return "*1"
        if self.building == "gimnazjum":
            return "*2"
        if self.building == "grobla":
            return ""
        return None

    def getClassIds(self):  #Pozyskiwanie id gabinetów dla konkretnego dnia (potencjalnie zmienić na wszystkie klasy?)
        classroomIds = list()
        for i in self.resdata['r']['dbiAccessorRes']['tables'][20]['data_rows']:
            if i['days'] == self.day and i['period'] == self.hour:
                classroomIds.append(i['classroomids'][0])
        if not classroomIds:
            return ""
        print(classroomIds)
        return classroomIds

    def getClassroomNames(self):    #Pozyskiwanie nazw gabinetów
        classroomNames = list()
        buildingId = self.getBuildingId()
        classroomIds = self.getClassIds()
        for i in self.resdata['r']['dbiAccessorRes']['tables'][11]['data_rows']:
            if i['id'] not in classroomIds and i['buildingid'] == buildingId:
                classroomNames.append(i['name'])
        classroomNames.sort()
        return classroomNames

    def createCodeBlockResponse(self, array):   #Formatowanie outputa jako discordowego bloku code w pionowej liście
        response = """```\n{}```""".format("\n".join(array))
        return response
