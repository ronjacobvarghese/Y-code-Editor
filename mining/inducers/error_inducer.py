import re
import shutil
import os
import random


class errors:

    def __init__(self, perFileError, noOfError):
        self.perFileError = perFileError
        self.noOfErr = noOfError

    def genError(self):

        error_types = [
            self.emptyLoop,
            self.removeReturn,
            self.equalityComparisonToAssignment,
            self.errors_in_assignment_operators,
            self.left_assignment_to_right,
            self.notypedeclaration,
        ]
        
        self.edit = 0
        no_of_errors = len(error_types)
        tempFileError = self.perFileError
        self.code = self.codeSnip
        itr = 0
        while self.noOfErr:
            error_types[random.randint(0, no_of_errors-1)]()
            if self.edit:
                tempFileError -= 1
                self.edit = 0
                self.noOfErr -=1
            if not tempFileError:
                itr+=1
                self.__fileWrite(self.code,"Error",itr)
                self.code = self.codeSnip
                tempFileError = self.perFileError
                
                
    def fileOpen(self, filename):
        if os.path.exists('../../test_codes/tests'):
            shutil.rmtree('../../test_codes/tests')
        os.mkdir('../../test_codes/tests')
        with open(filename, 'r', encoding='utf-8') as f:
            self.codeSnip = f.read()
            f.close()

        self.__detectOperators(self.codeSnip)
        self.__searchDatatype(self.codeSnip)
        self.__searchKeywords(self.codeSnip)

    def __fileWrite(self, errorSnip, error, no):
        with open(f'../../test_codes/tests/E_test_{error}_{no}', "w", encoding='utf-8') as f:
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

    def removeReturn(self):
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

    def equalityComparisonToAssignment(self):
        operatorsList = [(start, end) for start,
                         end in self.__operatorsList if self.codeSnip[start:end] == "=="]
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

    # [+=,-=,/=,%=]
    def errors_in_assignment_operators(self):
        operatorList = [(start, end) for start,
                        end in self.__operatorsList if self.codeSnip[start:end] not in ["*=", "/=", "=="]]
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

    def left_assignment_to_right(self):
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
                operatorsList.append((startPos, endPos,pos.start(),pos.end()))
        n = len(operatorsList)
        if not n:
            print("Error not found in left assignment to right.")
            return
        startPos, endPos , start, end= operatorsList[random.randint(0, n-1)]
        self.code = self.code.replace(
            self.codeSnip[startPos:endPos], f"{self.codeSnip[end:endPos]} = {self.codeSnip[startPos:start]}")
        self.edit = 1
        print("Left Assignment to Right: Success")

    def notypedeclaration(self):
        n = len(self.__datatypeList)
        if not n:
            print("Error not found in no type declaration.")
        start,end = self.__datatypeList[random.randint(0,n-1)]
        startPos = start
        while self.codeSnip[startPos] not in "{;":
            startPos -= 1
        startPos +=2
        endPos = end
        while self.codeSnip[endPos] != ";":
            endPos += 1
        self.code = self.code.replace(
            self.codeSnip[startPos:endPos], self.codeSnip[start:endPos])
        self.edit = 1
        print("No Type Declaration:Success")

    def else_if_concatenate(self, codesnip, t=2):
        for i in range(len(codesnip)):
            if "else if" in codesnip[i]:
                print(codesnip[i])


Err = errors(1, 6)
Err.fileOpen("../../test_codes/test_add.cpp")
Err.genError()

# codesnip=Err.fileopen()
# codesnip2=Err.equalityComparisontoAssignment(codesnip)
# Err.filewrite(codesnip2,"../../testcode/testcode_errors/testcode2.cpp")

# codesnip=Err.fileopen()
# codesnip2=Err.errors_in_assignment_operators(codesnip)
# Err.filewrite(codesnip2,"../../testcode/testcode_errors/testcode3.cpp")

# codesnip=Err.fileopen()
# codesnip2=Err.left_assignment_to_right(codesnip)
# Err.filewrite(codesnip2,"../../testcode/testcode_errors/testcode4.cpp")

# codesnip=Err.fileopen()
# codesnip2=Err.notypedeclaration(codesnip)
# Err.filewrite(codesnip2,"../../testcode/testcode_errors/testcode5.cpp")
