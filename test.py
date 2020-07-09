import pandas as pd
import os
# ['CHIISAI', 'KATACHI', 'SOPPO', 'BIBIRI', 'POKA', 'AJIKESHI', 'HOUCHI', 'IKKI', 'reigai', 'OTUKIAI']

anaGood = pd.read_csv('testAnaGoodDiff_new.csv')
names = anaGood.get('name')
rootFilePath = '/home/fan/GoProjects/Go_data/detection'
marked = ['BIBIRI', 'KATACHI', 'CHIISAI', 'SOPPO', 'OTUKIAI', 'AJIKESHI', 'IKKI', 'POKA', 'HOUCHI', 'reigai']

# for path, dir_list, file_list in os.walk(rootFilePath):
#     print(file_list)
#     for name in names:
#         # print(name)
#         sfgName = name + ".sgf"
#         sgfFile = rootFilePath+"/"+sfgName
#         if sfgName in file_list:
#             if os.path.exists(sgfFile):
#                 os.remove(sgfFile)
#

oldBadData = pd.read_csv('04071348bad.csv')
andBadData = pd.read_csv('testAnaBadDiff_new_new.csv')

count = 0
labels = []
labelsForPrint = []

for index, row in andBadData.iterrows():
    print(row['name'])
    name = row['name']
    moveNumber = row['move']
    found = False
    for index_old, row_old in oldBadData.iterrows():
        oldName = row_old['name']
        oldHandi = int(row_old['handi'])
        oldMoveNumber = int(row_old['move']) - 2*oldHandi
        if name == oldName and int(moveNumber) == oldMoveNumber:
            badClass = row_old['label2']
            if badClass not in labels:
                count = count + 1
                labelsForPrint.append(badClass)
            labels.append(marked.index(badClass))
            found = True
            break
    if not found:
        labels.append('not found')

andBadData['label'] = labels
andBadData.to_csv('badDataWithLabel_encoded_new.csv')
# print(count)
# print(labelsForPrint)

