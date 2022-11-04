import re
import shutil
import os
import random
import subprocess
from ..data_process.generate_dataset import generate_dataset as genData
from datetime import datetime

class errors:

    def __init__(self, perFileError, noOfError):
        self.perFileError = perFileError
        self.noOfErr = noOfError
        self.emptyLoop_count = 0
        self.removeReturn_count = 0
        self.equalityComparisonToAssignment_count = 0
        self.errors_in_assignment_operators_count = 0
        self.left_assignment_to_right_count = 0
        self.notypedeclaration_count = 0

    def errorStats(self):
        dateAndTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        currErrorStats = f'emptyLoop_count = {self.emptyLoop_count}\n removeReturn_count = {self.removeReturn_count}\n equalityComparisonToAssignment_count = {self.equalityComparisonToAssignment_count}\n errors_in_assignment_operators_count = {self.errors_in_assignment_operators_count}\n left_assignment_to_right_count = {self.left_assignment_to_right_count}\n notypedeclaration_count = {self.notypedeclaration_count}\n'
        with open('dataset/errorStats.txt','+a') as estat:
            estat.write(currErrorStats+dateAndTime)

    def genError(self):

        error_types = [
            self.emptyLoop,
            self.removeReturn,
            self.equalityComparisonToAssignment,
            self.errors_in_assignment_operators,
            self.left_assignment_to_right,
            self.notypedeclaration,
        ]
        itr = 0
        self.edit = 0
        no_of_errors = len(error_types)
        tempFileError = self.perFileError
        self.code = self.codeSnip
        errorNo = 0
        while self.noOfErr and itr != 50:
            print
            error_types[random.randint(0, no_of_errors-1)]()
            if self.edit:
                tempFileError -= 1
                self.edit = 0
                self.noOfErr -= 1
            else:
                itr += 1
            if not tempFileError:
                errorNo += 1
                if not os.path.exists(f'dataset/records/{self.folderNo}/error_codes'):
                    os.mkdir(f'dataset/records/{self.folderNo}/error_codes')
                if os.path.exists(f'dataset/{self.folderNo}/error_codes/{errorNo}'):
                    continue
                self.__fileWrite(self.code, errorNo)
                gD = genData()
                gD.createAST(f'dataset/records/{self.folderNo}/error_codes/{errorNo}/error.cpp',f'dataset/records/{self.folderNo}/error_codes/{errorNo}',errorNo)
                self.code = self.codeSnip
                tempFileError = self.perFileError
                print(
                    f"Ast Generated for folder:{self.folderNo} errorNo:{errorNo}")

    def fileOpen(self, folderNo):
        self.folderNo = folderNo
        with open(f"dataset/records/{folderNo}/code.cpp", 'r', encoding='utf-8') as f:
            self.codeSnip = f.read()
            f.close()

        self.__detectOperators(self.codeSnip)
        self.__searchDatatype(self.codeSnip)
        self.__searchKeywords(self.codeSnip)

    # def __genAst(self, errorSnip, errorNo):
    #     codeFile = '#include "precompiled.h"\n'
    #     headerFiles = []
    #     print("folder: ", errorNo)
    #     code = errorSnip
    #     findHeader = re.finditer('[ ]*#\s*include\s*[\"<][^>\"]*[\">]', code)
    #     tempCode = code
    #     for pos in findHeader:
    #         headerFiles.append(code[pos.start():pos.end()]+'\n')
    #         tempCode = tempCode.replace(code[pos.start():pos.end()], "")
    #     codeFile += tempCode
    #     with open("precompiled.h", 'w+') as pFile:
    #         pFile.writelines(headerFiles)
    #     s = subprocess.run(
    #         "clang -x c++-header precompiled.h -Xclang -emit-pch -o precompiled.h.pch", shell=True)
    #     with open("temp.cpp", 'w+') as tempFile:
    #         tempFile.write(codeFile)
    #     s = subprocess.run(
    #         f"clang -Xclang -ast-dump=json -fsyntax-only -Wno-register -include-pch precompiled.h.pch temp.cpp > ../../dataset/{self.folderNo}/error_codes/{errorNo}/error_ast.json", shell=True)

    def __fileWrite(self, errorSnip, folder):
        if os.path.exists(f'dataset/records/{self.folderNo}/error_codes/{folder}'):
            print("Error Already Exists")
            return
        os.mkdir(f'dataset/records/{self.folderNo}/error_codes/{folder}')
        with open(f'dataset/records/{self.folderNo}/error_codes/{folder}/error.cpp', "w+", encoding='utf-8') as f:
            f.write("".join(errorSnip))
            f.close()

    def __detectOperators(self, codeSnip):
        self.__operatorsList = []
        searchOperators = re.finditer('(==|<=|>=|!=|\*=|\/=|\+=|-=)', codeSnip)
        for pos in searchOperators:
            startPos = pos.start()
            endPos = pos.end()
            self.__operatorsList.append((startPos, endPos))
        # print(self.__operatorsList)

    def __searchDatatype(self, codeSnip):
        self.__datatypeList = []
        searchDatatype = re.finditer(
            '(\s|;)(int|bool|float|double|char)\s', codeSnip)
        # print(list(searchDatatype))
        for i in searchDatatype:
            end = i.end()
            l = 0
            while codeSnip[end] not in ";":
                if codeSnip[end] == '{':
                    l = 1
                    break
                end += 1
            if l:
                continue
            self.__datatypeList.append((i.end(), end))

    def __searchKeywords(self, codeSnip):
        self.__findKeywords = []
        searchReturn = re.finditer(
            '(\s|;)(return\s|for\(|for \(|while\(|while \()', codeSnip)
        for i in searchReturn:
            self.__findKeywords.append((i.start()+1, i.end()))

    def emptyLoop(self):
        try:
            findKeywords = [(start, end) for start,
                            end in self.__findKeywords if self.codeSnip[end-1] == "("]
            n = len(findKeywords)
            if not n:
                print("error not found in emtpy loop")
                return
            start, end = findKeywords[random.randint(0, n-1)]
            startPos = end
            while self.codeSnip[startPos] != "{":
                startPos += 1
            endPos = startPos
            while self.codeSnip[endPos] != "}":
                endPos += 1
            self.code = self.code.replace(self.codeSnip[startPos:endPos+1], "")
            self.edit = 1
            print("Empty Loop: Success")
            self.emptyLoop_count += 1
        except:
            print("Empty Loop Process Failed")
            self.edit = 0

    def removeReturn(self):
        try:
            findKeywords = [(start, end) for start,
                            end in self.__findKeywords if self.codeSnip[start:end-1] == "return"]
            n = len(findKeywords)
            if not n:
                print("Error not found in removeReturn")
                return
            start, end = findKeywords[random.randint(0, n-1)]
            startPos = start
            while self.codeSnip[startPos] not in "{;":
                startPos -= 1
            startPos += 1
            endPos = end
            while self.codeSnip[endPos] not in "{;":
                endPos += 1
            self.code = self.code.replace(self.codeSnip[startPos:endPos+1], "")
            self.edit = 1
            print("Remove Return:Success")
            self.removeReturn_count += 1
        except:
            print("Remove Return Process Failed")
            self.edit = 0

    def equalityComparisonToAssignment(self):
        try:
            operatorsList = [
                (start, end) for start, end in self.__operatorsList if self.codeSnip[start:end] == "=="]
            n = len(operatorsList)
            if not n:
                print("Error not found in equality Comparison To assignment.")
                return
            start, end = operatorsList[random.randint(0, n-1)]
            startPos = start
            while self.codeSnip[startPos] not in "{;":
                startPos -= 1

            endPos = end
            while self.code[endPos] != ";":
                endPos += 1

            self.code = self.code.replace(
                self.codeSnip[startPos:endPos], f'{self.codeSnip[startPos:end-1]}{self.codeSnip[end:endPos]}')
            self.edit = 1
            print("Equality Comparison To Assignments:Success")
            self.equalityComparisonToAssignment_count += 1
        except:
            print("Equality Comparison TO assignment: Failed")
            self.edit = 0
    # [+=,-=,/=,%=]

    def errors_in_assignment_operators(self):
        try:
            operatorList = [(start, end) for start, end in self.__operatorsList if self.codeSnip[start:end] not in ["*=", "/=", "=="]]
            n = len(operatorList)
            if not n:
                print("Error not found in errors in assignments operators.")
                return
            start, end = operatorList[random.randint(0, n-1)]
            startPos = start
            while self.codeSnip[startPos] not in ";{":
                startPos -= 1
            endPos = end
            while self.codeSnip[endPos] != ";":
                endPos += 1
            self.code = self.code.replace(
                self.codeSnip[startPos:endPos], f"{self.codeSnip[startPos:start]} {self.codeSnip[end-1]}{self.codeSnip[start]} {self.codeSnip[end:endPos]} ")
            self.edit = 1
            print("Errors In Assigment Operators: Success")
            self.errors_in_assignment_operators_count += 1
        except:
            print("Errors in Assignment Operator: Failed")
            self.edit = 0

    def left_assignment_to_right(self):
        try:
            equalLoc = re.finditer("=", self.codeSnip)
            operatorsList = []
            for pos in equalLoc:
                l = 0
                for start, end in self.__operatorsList:
                    if pos.start() >= start and pos.end() <= end:
                        l = 1
                        break
                if l:
                    continue
                startPos = pos.start()
                l = 0
                while self.codeSnip[startPos] not in "{;":
                    startPos -= 1
                startPos += 1
                endPos = pos.end()
                while self.codeSnip[endPos] not in "{;":
                    if self.codeSnip[endPos] in "+" and self.codeSnip[endPos+1] != "+":
                        l = 1
                    if self.codeSnip[endPos] in "-" and self.codeSnip[endPos+1] != "-":
                        l = 1
                    if self.codeSnip[endPos] in "*/":
                        l = 1
                    endPos += 1
                if not l:
                    continue
                else:
                    operatorsList.append(
                        (startPos, endPos, pos.start(), pos.end()))
            n = len(operatorsList)
            if not n:
                print("Error not found in left assignment to right.")
                return
            startPos, endPos, start, end = operatorsList[random.randint(
                0, n-1)]
            self.code = self.code.replace(
                self.codeSnip[startPos:endPos], f"{self.codeSnip[end:endPos]} = {self.codeSnip[startPos:start]}")
            self.edit = 1
            print("Left Assignment to Right: Success")
            self.left_assignment_to_right_count += 1
        except:
            print("Left Assignment to Right: Failed")
            self.edit = 0

    def notypedeclaration(self):
        try:
            n = len(self.__datatypeList)
            if not n:
                print("Error not found in no type declaration.")
            start, end = self.__datatypeList[random.randint(0, n-1)]
            startPos = start
            while self.codeSnip[startPos] not in "{;":
                startPos -= 1
            startPos += 2
            endPos = end
            while self.codeSnip[endPos] != ";":
                endPos += 1
            self.code = self.code.replace(
                self.codeSnip[startPos:endPos], self.codeSnip[start:endPos])
            self.edit = 1
            print("No Type Declaration:Success")
            self.notypedeclaration_count += 1
        except:
            print("No Type Declaration: Failed")

    def else_if_concatenate(self, codesnip, t=2):
        for i in range(len(codesnip)):
            if "else if" in codesnip[i]:
                print(codesnip[i])



folders = os.listdir('dataset/records')
for i in folders:
    try:
        Err = errors(1, 10)
        Err.fileOpen(i)
        Err.genError()
    except KeyboardInterrupt:
        print("some keyboard interrupt")
        Err.errorStats()

