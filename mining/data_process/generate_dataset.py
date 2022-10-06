import csv
import os
from re import sub
import subprocess
import re
import shutil

class generate_dataset:

    def createSampleCsv(self):
        sampleCodes = []
        noOfCodes = 2000
        with open("code_snippets_OK.csv",'r+') as csvFile:
            csvReader = csv.reader(csvFile)
            for codeData in csvReader:
                sampleCodes.append(codeData)
                noOfCodes-=1
                if noOfCodes==0:
                    break
        with open("sample305.csv",'w+') as sampCsv:
                        csvWriter = csv.writer(sampCsv)
                        csvWriter.writerows(sampleCodes)


    def workingCodeFilter(self):
        correctCodeCounter = 1
        codeCounter = 1
        filteredCodes = []
        with open("sample305.csv",'r+') as codeCsv:
            csvReader = csv.reader(codeCsv)
            for codeData in csvReader:
                with open("test_code.cpp",'w+') as cFile:
                    cFile.write(codeData[2])
                with open("test_cases.csv", 'r+') as testCaseCsv:
                    testCaseData = csv.reader(testCaseCsv)
                    for testCase in testCaseData:
                        if testCase[0] == codeData[0] and testCase[1] == codeData[1]:
                            curTestCase = testCase[2]
                data, temp = os.pipe()
                os.write(temp, bytes(curTestCase,"utf-8"))
                os.close(temp)
                print("codeNo: "+str(codeCounter))
                codeCounter+=1
                try:
                    try:
                        s = subprocess.check_output("g++ test_code.cpp; ./a.out", stdin=data, shell=True,timeout=5)
                    except(subprocess.TimeoutExpired):
                        print("code time out")
                        continue
                    filteredCodes.append(codeData)
                    print("correctCode: {}".format(correctCodeCounter))
                    correctCodeCounter +=1
                except:
                    print("not able to pass..")

        with open("working_codes.csv",'w+') as newCodeCsv:
                        csvWriter = csv.writer(newCodeCsv)
                        csvWriter.writerows(filteredCodes)


    def correctCodeGenerator(self):
        folderNo = 0
        # opening csv file for codesnipets
        with open("working_codes.csv",'r+') as codeCsv:
            csvReader = csv.reader(codeCsv)
            # if os.path.exists('../../dataset'):
            #     shutil.rmtree('../../dataset')
            # os.mkdir("../../dataset")
            for codeData in csvReader:
                # making directories for each correct codesnips
                if os.path.exists("../../dataset/"+str(folderNo)):
                    print(f"FOLDER ALREADY EXISTS {folderNo}")
                    folderNo+=1
                    continue
                os.mkdir("../../dataset/"+str(folderNo))
                # creating cpp files for each codesnips
                cppFileName = "../../dataset/"+str(folderNo)+"/code.cpp"
                with open(cppFileName,"w+") as cFile:
                    cFile.write(codeData[2])  
                folderNo+=1              
        return folderNo
    
    def createAST(self,totalFolders):
        for folderNo in range(totalFolders):
            if os.path.exists(f"../../dataset/{folderNo}/code_ast.json"):
                    print(f"JSON ALREADY EXISTS {folderNo}")
                    continue
            codeFile = '#include "precompiled.h"\n'
            headerFiles = []
            print("folder: ",folderNo)
            with open("../../dataset/"+str(folderNo)+"/code.cpp",'r+') as cFile:
                code = cFile.read()
                findHeader = re.finditer('[ ]*#\s*include\s*[\"<][^>\"]*[\">]',code)
                tempCode = code
                for pos in findHeader:
                    headerFiles.append(code[pos.start():pos.end()]+'\n')
                    tempCode = tempCode.replace(code[pos.start():pos.end()],"")
                codeFile+=tempCode
            with open("precompiled.h",'w+') as pFile:
                pFile.writelines(headerFiles)
            s = subprocess.run("clang -x c++-header precompiled.h -Xclang -emit-pch -o precompiled.h.pch",shell=True)
            with open("temp.cpp",'w+') as tempFile:
                tempFile.write(codeFile)
            s = subprocess.run(f"clang -Xclang -ast-dump=json -fsyntax-only -Wno-register -include-pch precompiled.h.pch temp.cpp > ../../dataset/"+str(folderNo)+"/code_ast.json",shell=True)
                    

d = generate_dataset()
d.createSampleCsv()
d.workingCodeFilter()
x = d.correctCodeGenerator()
d.createAST(x)
subprocess.run('python3 ../inducers/error_inducer.py',shell=True)