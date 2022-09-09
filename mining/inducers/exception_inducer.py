import random
import re

class ExceptionInducer:

    def fileOpen(self,fileName):
        with open(fileName, 'r+') as rfile:
            self.codeSnip = rfile.read()
            rfile.close()
            
        isBalanced = self.__checkParanthesis(self.codeSnip)
        
        if(not isBalanced[0]):
            print("Error:" + isBalanced[-1])
            exit(1)
        else:
            print("Success: " + isBalanced[-1])
            
        self.__searchKeywords(self.codeSnip)
    
    
    def __fileWrite (self, excSnip, exc, itr):
        with open(f'../../test_codes/tests/X_test_{exc}_{itr}', 'w') as wfile:
            wfile.write(excSnip)
            wfile.close()
        
            

    def  __checkParanthesis(self, codeSnip):
        stack = []
        self.__brackets = {}

        opening = '(['
        closing = ')]'

        for charIndex in range(len(codeSnip)):
            char = codeSnip[charIndex]
            if char == '}' and stack:
                return (False, "Check char {}".format(stack.pop()[0]))
            if char in opening:
                stack.append((charIndex, char))
            if char in closing:
                if not stack:
                    return (False, "No Opening Bracket for closing bracket at Char {}".format(char))

                if ((char == ")" and stack[-1][1] == "(") or
                        (char == ']' and stack[-1][1] == '[')):
                    self.__brackets[stack.pop()] = (charIndex, char)
                else:
                    return False

        if stack:
            print(stack)
            return (False, "Brackets UnBalanced Char:{}".format(stack.pop()[0]))

        return (True, "Brackets are Balanced!!")
    
    
    def __searchKeywords(self, codeSnip):
        self.__keywordsList = []
        searchDatatype = re.finditer('(int|bool|float|double|char\b)\s',codeSnip)
        # print(list(searchDatatype))
        for i in searchDatatype:
            end = i.end();l = 0
            while codeSnip[end] not in "(;":
                if codeSnip[end] == '{':
                    l = 1
                    break
                end+=1
            if l:
                continue
            self.__keywordsList.append((i.end(),end))
            
                                    
    def sqrtExc(self, perFileExceptions = 10, noOfExc = 20):
        itr = 0; edit = 0
        n = len(self.codeSnip)
        while noOfExc:
            code = self.codeSnip
            tempFileExceptions =perFileExceptions
            locSqrt = list(re.finditer('sqrt\(', code))
            tempSnip = code
            for i in range(len(locSqrt)):
                sqrtPtr = locSqrt[i]
                startPos = sqrtPtr.start()
                endPos = self.__brackets[(startPos+4,code[startPos+4])][0]+1
                tempSnip = tempSnip.replace(code[startPos:endPos],'sqrt({})'.format(random.randrange(-999999999,-1)))
                tempFileExceptions -=1
                noOfExc -=1
                edit = 1
                if not tempFileExceptions:
                    itr+=1
                    tempFileExceptions = perFileExceptions
                    self.__fileWrite(tempSnip, "SqrtNeg",itr)
                    tempSnip = code
                    edit = 0
                if not noOfExc:
                    itr += 1
                    self.__fileWrite(tempSnip, "SqrtNeg",itr)
                    edit = 0
                    return 
            if edit:
                self.__fileWrite(tempSnip, "SqrtNeg",itr)

    def indexExc(self, perFileExceptions = 10, noOfExc = 20):
        itr = 0
        while noOfExc:
            edit = 0
            code = self.codeSnip
            tempFileExceptions = perFileExceptions
            tempCode = code
            arrloc = re.finditer('[a-zA-Z_][a-zA-Z0-9_]*\[',code)
            for pos in arrloc:
                startpos = pos.start();l = 0
                endpos = self.__brackets[(pos.end()-1,code[pos.end()-1])][0]
                for s,e in self.__keywordsList:
                    if startpos >= s and endpos < e:
                        l = 1
                if l:
                    continue
                tempCode = tempCode.replace(code[startpos:endpos+1],f'{code[startpos:pos.end()]}{random.randint(10**9,10**11)}]')
                edit = 1
                tempFileExceptions -= 1
                noOfExc -=1
                if not tempFileExceptions:
                    itr+=1
                    self.__fileWrite(tempCode, "indexOut",itr)
                    tempFileExceptions = perFileExceptions
                    tempCode = code
                    edit = 0
                if not noOfExc:
                    itr+=1
                    self.__fileWrite(tempCode, "indexOut", itr)
                    edit = 0
                    return
            if edit:
                itr+=1
                self.__fileWrite(tempCode, "indexOut", itr)
            break
                            
    
            
    def dividebyzero(self, perFileExceptions = 10, noOfExc = 20):
        itr = 0
        n = len(self.codeSnip)
        while noOfExc:
            edit = 0
            code = self.codeSnip
            tempFileExceptions = perFileExceptions
            locCout = re.finditer('cout', code)
            for pos in locCout:
                startpos = pos.start()
                while self.codeSnip[startpos] != '<':
                    startpos+=1
                startpos+=2
                endpos = startpos
                while self.codeSnip[endpos] not in "<;":
                    endpos+=1
                code = code.replace(self.codeSnip[pos.start():endpos],f'{self.codeSnip[pos.start():startpos]}{self.codeSnip[startpos:endpos].strip()}/0')
                edit =1 
                tempFileExceptions -=1
                noOfExc -=1
                if not tempFileExceptions:
                    itr +=1
                    self.__fileWrite(code, "divideByZero", itr)
                    tempFileExceptions = perFileExceptions
                    code = self.codeSnip
                    edit= 0
                if not noOfExc:
                    itr +=1
                    self.__fileWrite(code, "divideByZero", itr)
                    edit = 0
                    return 
            if edit:
                itr +=1
                self.__fileWrite(code, "divideByZero", itr)
            break
                
                    

    def error_funcName(self, perFileExceptions = 10, noOfExc = 20):
        itr = 0
        while noOfExc:
            edit = 0
            code = self.codeSnip
            tempFileExceptions = perFileExceptions
            locFunc = set(re.finditer('[a-zA-Z_][a-zA-Z0-9_]*\(', code))
            for pos in locFunc:
                startpos = pos.start()
                endpos = pos.end() - 1

                l = 0
                for start,end in self.__keywordsList:
                    
                    if startpos>= start and endpos <= end:
                            l = 1
                if l:
                    continue
                sp = startpos + random.randint(0,endpos-startpos)
                while self.codeSnip[endpos] != ')':
                    endpos+=1
                code = code.replace(self.codeSnip[startpos:endpos],f'{self.codeSnip[startpos:sp]}{self.codeSnip[sp].swapcase()}{self.codeSnip[sp+1:endpos]}')
                edit =1 
                tempFileExceptions -=1
                noOfExc -=1
                if not tempFileExceptions:
                     itr +=1
                     self.__fileWrite(code, "wrongFunc", itr)
                     tempFileExceptions = perFileExceptions
                     code = self.codeSnip
                     edit = 0
                if not noOfExc:
                    itr += 1
                    self.__fileWrite(code, "wrongFunc", itr)
                    edit = 0
                    return
            if edit:
                itr+=1
                self.__fileWrite(code, "wrongFunc", itr)
            break
    
                
        
            
            

exc = ExceptionInducer()
exc.fileOpen('../../test_codes/test_add.cpp')
exc.error_funcName(1)
