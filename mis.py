import os
import shutil
rootPath = '/home/fan/GoProjects/katago_Tools/'
path1 = 'dec_ana'
path2 = 'ana_report_backup'

for anaFile_ in os.listdir(rootPath+path2):
    if not os.path.isdir(anaFile_):
        forRemoveFileName = rootPath+path1+"/"+ str(anaFile_)[:-7]
        print(forRemoveFileName)
        shutil.rmtree(forRemoveFileName)