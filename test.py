import pandas as pd
import os

anaGood = pd.read_csv('testAnaGoodDiff_new.csv')
names = anaGood.get('name')
rootFilePath = '/home/fan/GoProjects/Go_data/detection'


for path, dir_list, file_list in os.walk(rootFilePath):
    print(file_list)
    for name in names:
        # print(name)
        sfgName = name + ".sgf"
        sgfFile = rootFilePath+"/"+sfgName
        if sfgName in file_list:
            if os.path.exists(sgfFile):
                os.remove(sgfFile)


