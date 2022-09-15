import code
import re
import shutil
import os


class errors:

    def fileOpen(self, filename):
        if os.path.exists('../../test_codes/tests'):
            shutil.rmtree('../../test_codes/tests')
        os.mkdir('../../test_codes/tests')
        with open(filename, 'r', encoding='utf-8') as f:
            self.codeSnip1 = f.read()
            f.close()
        with open(filename, 'r', encoding='utf-8') as f:
            self.codeSnip2 = f.readlines()
            f.close()

        self.__detectOperators(self.codeSnip1)
        self.__searchKeywords(self.codeSnip1)

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
        
    def __searchKeywords(self, codeSnip):
        self.__keywordsList = []
        searchDatatype = re.finditer(
            '(int|bool|float|double|char\b)\s', codeSnip)
        # print(list(searchDatatype))
        for i in searchDatatype:
            end = i.end()
            l = 0
            while codeSnip[end] not in "(;":
                if codeSnip[end] == '{':
                    l = 1
                    break
                end += 1
            if l:
                continue
            self.__keywordsList.append((i.end(), end))

    def emptyLoop(self, perFileError=10, noOfErr=20):
        itr = 0
        filePtr = 0
        n = len(self.codeSnip)
        while noOfErr and filePtr != n:
            code = self.codeSnip.copy()
            a = ["while", "for"]
            edit = 0
            tempFileError = perFileError

            for i in range(filePtr, len(code)):
                filePtr = i+1
                # if "while" in code[i]:
                if any(x in code[i] for x in a):
                    edit = 1
                    tmp = list(code[i])

                    for j in range(len(tmp)):
                        if tmp[j] == ")":
                            tmp = tmp[0:j+1]+[";"]+tmp[j+1:]
                            break
                    code.pop(i)
                    code.insert(i, "".join(tmp))
                    noOfErr -= 1
                    tempFileError -= 1
                if not tempFileError:
                    itr += 1
                    break
            if edit:
                self.__fileWrite(code, "EmptyLoop", itr)

    def removeReturn(self, codeSnip, noOfErr=2):
        codeSnip = codeSnip.readlines()
        pass

    def equalityComparisonToAssignment(self, perFileError=10, noOfErr=20):
        itr = 0
        code = self.codeSnip1
        tempFileErrors = perFileError
        edit = 0
        for start, end in self.__operatorsList:
            if self.codeSnip1[start:end] != "==":
                continue
            startPos = start
            while self.codeSnip1[startPos] not in ";":
                startPos -= 1

            endPos = end
            while code[endPos] != ";":
                endPos += 1

            code = code.replace(
                self.codeSnip1[startPos:endPos], f'{self.codeSnip1[startPos:end-1]}{self.codeSnip1[end:endPos]}')
            tempFileErrors -= 1
            noOfErr -= 1
            edit = 1
            if not tempFileErrors:
                itr += 1
                tempFileErrors = perFileError
                self.__fileWrite(code, "compErr", itr)
                code = self.codeSnip1
                edit = 0
            if not noOfErr:
                itr += 1
                self.__fileWrite(code, 'compErr', itr)
                edit = 0
                return
        if edit:
            itr += 1
            self.__fileWrite(code, "compErr", itr)

    # [+=,-=,/=,%=]
    def errors_in_assignment_operators(self, perFileErrors, noOfErr=20):
        itr = 0
        code = self.codeSnip1
        tempFileErrors = perFileErrors
        edit = 0
        for start, end in self.__operatorsList:
            if self.codeSnip1[start:end] not in ["*=", "/="]:
                continue
            startPos = start
            while self.codeSnip1[startPos] not in ";{":
                startPos -= 1
            endPos = end
            while self.codeSnip1[endPos] != ";":
                endPos += 1
            code = code.replace(
                self.codeSnip1[startPos:endPos], f"{self.codeSnip1[startPos:start]} {self.codeSnip1[end-1]}{self.codeSnip1[start]} {self.codeSnip1[end:endPos]} ")
            tempFileErrors -= 1
            noOfErr -= 1
            edit = 1
            if not tempFileErrors:
                itr += 1
                tempFileErrors = perFileErrors
                self.__fileWrite(code, "assignErr", itr)
                code = self.codeSnip1
                edit = 0
            if not noOfErr:
                itr += 1
                self.__fileWrite(code, "assignErr", itr)
                edit = 0
                return
        if edit:
            itr += 1
            self.__fileWrite(code, "assignErr", itr)

    def left_assignment_to_right(self, perFileErrors, noOfErr = 20):
        itr = 0
        code =self.codeSnip1
        tempFileErrors = perFileErrors
        edit = 0
        equalLoc = re.finditer("=", self.codeSnip1)
        for pos in equalLoc:
            l = 0
            for start,end in self.__operatorsList:
                if pos.start() >= start and pos.end() <= end:
                    l = 1
                    break
            if l:
                continue
            startPos = pos.start()
            l = 0
            while self.codeSnip1[startPos] not in "{;":
                startPos -= 1
            startPos +=1
            endPos = pos.end()
            while self.codeSnip1[endPos] not in ";":
                if self.codeSnip1[endPos] in "+" and self.codeSnip1[endPos+1] != "+":
                    l = 1
                if self.codeSnip1[endPos] in "-" and self.codeSnip1[endPos+1] != "-":
                    l  = 1
                if self.codeSnip1[endPos] in "*/":
                    l = 1
                endPos +=1    
            if not l:
                continue
            code = code.replace(self.codeSnip1[startPos:endPos], f"{self.codeSnip1[pos.end():endPos]} = {self.codeSnip1[startPos:pos.start()]}")
            tempFileErrors -=1
            noOfErr -=1
            edit = 1
            if not tempFileErrors:
                itr +=1
                tempFileErrors = perFileErrors
                self.__fileWrite(code,"invertAssign",itr)
                code = self.codeSnip1
                edit  = 0
            if not noOfErr:
                itr +=1
                self.__fileWrite(code, "invertAssign", itr)
                edit = 0
                return
        if edit:
            itr +=1
            self.__fileWrite(code, "inertAssign", itr)
            

    def notypedeclaration(self, perFileErrors, noOfErr = 20):
        itr  = 0
        code = self.codeSnip1
        tempFileErrors = perFileErrors
        edit = 0
        for start, end in self.__keywordsList:
            startPos = start
            while self.codeSnip1[startPos] not in "{;":
                startPos -=1
            endPos = end
            while self.codeSnip1[endPos] != ";":
                endPos+=1
            code = code.replace(self.codeSnip1[startPos:endPos],self.codeSnip1[start:endPos])
            tempFileErrors -=1
            noOfErr -=1
            edit = 1
            if not tempFileErrors:
                itr +=1
                tempFileErrors = perFileErrors
                self.__fileWrite(code,"notDec",itr)
                code = self.codeSnip1
                edit = 0
            if not noOfErr:
                itr +=1
                self.__fileWrite(code,"notDec",itr)
                edit = 0
                return 
        if edit:
            itr +=1
            self.__fileWrite(code,"notDec",itr)
            

    def else_if_concatenate(self, codesnip, t=2):
        for i in range(len(codesnip)):
            if "else if" in codesnip[i]:
                print(codesnip[i])


Err = errors()
codesnip = Err.fileOpen("../../test_codes/test_add.cpp")
Err.notypedeclaration(1)

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
