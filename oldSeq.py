# 1 - get class id
className = "4tp"
classId = ''
for i in resdata['r']['dbiAccessorRes']['tables'][12]['data_rows']:
    if '4Tp' in i['name']:
        classId = i['id']
        break

# 2 - get lessonIds
lessonIds = list()
subjectNames = list()
for i in resdata['r']['dbiAccessorRes']['tables'][18]['data_rows']:
    if classId in i['classids']:
        lessonIds.append(i['id'])
        for j in resdata['r']['dbiAccessorRes']['tables'][13]['data_rows']:
            if j['id'] == i['subjectid']:
                subjectNames.append(j['name'])
                break

# 3 - get lessons for specific day and sort them
days = 0
for i in resdata['r']['dbiAccessorRes']['tables'][20]['data_rows']:
    if i['days'] == "10000" and i['lessonid'] in lessonIds:
        days += 1
lessonsForTheDay = ['None'] * days
for i in resdata['r']['dbiAccessorRes']['tables'][20]['data_rows']:
    if i['days'] == "10000" and i['lessonid'] in lessonIds:
        lessonsForTheDay[int(i['period']) - 1] = subjectNames[(lessonIds.index(i['lessonid']))] + ', '