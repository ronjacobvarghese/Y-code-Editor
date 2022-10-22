import csv
import os
from re import sub
import subprocess
import re
import shutil

class generate_dataset:
    def __init__(self):
        self.correctCodeCounter = 0
        self.codeCounter = 0
        self.wrongCodeCounter = 0


    def genDataset(self,fileName):
        with open(fileName,"r+") as r_file:
            codeFile = csv.reader(r_file)
            for codeData in codeFile:
                isValidCode = self.workingCodeFilter(codeData[0]+codeData[1],codeData[2])
                if not isValidCode:
                    continue
                if not os.path.exists("../../dataset"):
                    os.mkdir("../../dataset")
                if not os.path.exists("../../dataset/records"):
                    os.mkdir("../../dataset/records")
                isGenerated = self.correctCodeGenerator(codeData[2])
                if isGenerated:
                    continue
                self.createAST("../../dataset/records/"+str(self.correctCodeCounter)+"/code.cpp","../../dataset/records/"+str(self.correctCodeCounter))



    def createSampleCsv(self):
        noOfCodes = 200
        with open("../../codeforces/code_snippets/code_snippets_OK.csv",'r+') as csvFile:
            csvReader = csv.reader(csvFile)
            for codeData in csvReader:
                if noOfCodes==0:
                    return
                with open("../../codeforces/code_snippets/sample.csv",'+a') as sampCsv:
                        sampWriter = csv.writer(sampCsv)
                        sampWriter.writerow(codeData)
                noOfCodes -= 1


    def workingCodeFilter(self,codeId, codeSnip):
    
        with open("../../codeforces/test_cases/test_cases.csv") as testCaseCsv:
            testCaseData = csv.reader(testCaseCsv)
            for testCase in testCaseData:
                testId = testCase[0] + testCase[1]
                if testId == codeId:
                    test = testCase[2]
            with open("./tests/test_code.cpp",'w+') as cFile:
                    cFile.write(codeSnip)
                    
            data,temp = os.pipe()
            os.write(temp,bytes(test,"utf-8"))
            os.close(temp)
            self.codeCounter+=1
            print("codeNO: "+str(self.codeCounter))

        # #iterative code working filter
        # correctCodeCounter = 1
        # codeCounter = 1
        # filteredCodes = []
        # with open("sample305.csv",'r+') as codeCsv:
        #     csvReader = csv.reader(codeCsv)
        #     for codeData in csvReader:
        #         with open("test_code.cpp",'w+') as cFile:
        #             cFile.write(codeData[2])
        #         with open("test_cases.csv", 'r+') as testCaseCsv:
        #             testCaseData = csv.reader(testCaseCsv)
        #             for testCase in testCaseData:
        #                 testId = testCase[0]+testCase[1]
        #                 if testId == codeId:
        #                     curTestCase = testCase[2]
                    # data, temp = os.pipe()
                    # os.write(temp, bytes(curTestCase,"utf-8"))
                    # os.close(temp)
                    # codeCounter+=1
                    # print("codeNo: "+str(codeCounter))
            try:
                try:
                    s = subprocess.check_output("g++ tests/test_code.cpp -o ./tests/a.out; ./tests/a.out", stdin=data, shell=True,timeout=5)
                except(subprocess.TimeoutExpired):
                    print("code time out")
                    self.wrongCodeCounter +=1
                    return False
                self.correctCodeCounter +=1
                print("correctCode: {}".format(self.correctCodeCounter))
                return True

            except:
                print("not able to pass..")

    def correctCodeGenerator(self,codeSnip):
        if os.path.exists("../../dataset/records/"+str(self.correctCodeCounter)):
            print(f"FOLDER ALREADY EXISTS {self.correctCodeCounter}")
            return True
        os.mkdir("../../dataset/records/"+str(self.correctCodeCounter))
        cppFileName = "../../dataset/records/"+str(self.correctCodeCounter)+"/code.cpp"
        with open(cppFileName,"w+") as cFile:
            cFile.write(codeSnip)  
        return False
        # opening csv file for codesnipets
        
    
    def createAST(self,readLoc,genLoc):
            codeFile = '#include "precompiled.h"\n'
            headerFiles = []
            print("folder: ",self.correctCodeCounter)
            with open(readLoc,'r+') as cFile:
                code = cFile.read()
                findHeader = re.finditer('[ ]*#\s*include\s*[\"<][^>\"]*[\">]',code)
                tempCode = code
                for pos in findHeader:
                    headerFiles.append(code[pos.start():pos.end()]+'\n')
                    tempCode = tempCode.replace(code[pos.start():pos.end()],"")
                codeFile+=tempCode
            with open("tests/precompiled.h",'w+') as pFile:
                pFile.writelines(headerFiles)
            s = subprocess.run("clang -x c++-header tests/precompiled.h -Xclang -emit-pch -o tests/precompiled.h.pch",shell=True)
            with open("tests/temp.cpp",'w+') as tempFile:
                tempFile.write(codeFile)
            s = subprocess.run(f"clang -Xclang -ast-dump=json -fsyntax-only -Wno-register -include-pch tests/precompiled.h.pch tests/temp.cpp >" + genLoc + "/code_ast.json",shell=True)
                    

d = generate_dataset()
d.createSampleCsv()
d.genDataset("../../codeforces/code_snippets/sample.csv")
subprocess.run('python3 ../inducers/error_inducer.py',shell=True)