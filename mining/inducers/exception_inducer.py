import random
import re

class ExceptionInducer:

    def fileOpen(self,fileName):
        with open(fileName, 'r+') as rfile:
            self.codeSnip2 = rfile.readlines()
            rfile.close()
        with open(fileName, 'r+') as rfile:
            self.codeSnip1 = rfile.read()
            rfile.close()
        print(self.codeSnip1,self.codeSnip2)
            
        isBalanced = self.__checkParanthesis(self.codeSnip1)
        
        if(not isBalanced[0]):
            print("Error:" + isBalanced[-1])
            exit(1)
        else:
            print("Success: " + isBalanced[-1])
    
    
    def __fileWrite (self, excSnip, exc, itr):
        with open(f'../../test_codes/X_test_{exc}_{itr}', 'w') as wfile:
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
    
    
    def __searchKeyword(self, codeSnip):
        self.__wordMap = []
        print(codeSnip)
        searchDatatype = re.finditer('[\( ](int|bool|float|double|char\b)\s',codeSnip)
        # print(list(searchDatatype))
        for i in searchDatatype:
            end = i.end()
            while codeSnip[end] != ";":
                end+=1
            self.__wordMap.append((i.end(),end))
                                    
    def sqrtExc(self, perFileExceptions = 10, noOfExc = 20):
        itr = 0; filePtr = 0; edit = 0
        n = len(self.codeSnip1)
        while noOfExc:
            code = self.codeSnip1
            tempFileExceptions =perFileExceptions
            locSqrt = list(re.finditer('sqrt\(', code))
            tempSnip = code
            for i in range(filePtr, len(locSqrt)):
                filePtr = i+1
                sqrtPtr = locSqrt[i]
                startPos = sqrtPtr.start()
                endPos = self.__brackets[(startPos+4,code[startPos+4])][0]+1
                tempSnip = tempSnip.replace(code[startPos:endPos],'sqrt({})'.format(random.randrange(-999999999,-1)))
                tempFileExceptions -=1
                noOfExc -=1
                edit = 1
                if not tempFileExceptions or not noOfExc:
                    itr+=1
                    break
            if edit:
                self.__fileWrite(tempSnip, "SqrtNeg",itr)
            if filePtr == len(locSqrt):
                break

    def indexExc(self, perFileExceptions = 10, noOfExc = 20):
        itr = 0;filePtr = 0;
        n = len(self.codeSnip2)
        while noOfExc and filePtr != n:
            edit = 0
            code = self.codeSnip2.copy()
            tempFileExceptions = perFileExceptions
            for i in range(len(code)):
                filePtr = i+1
                validtype = True
                for datatype in ['int','char','float','bool']:
                    if datatype in code[i]:
                        validtype = False
                # validtype = re.search('(\s+(int|char|bool|float)|^(int|char|bool|float))\s+',code[i])
                validarr = re.search('[a-zA-Z_][a-zA-Z0-9_]*\[',code[i])
                if validtype and validarr:
                    arrloc = re.finditer('[a-zA-Z_][a-zA-Z0-9_]*\[',code[i])
                    for pos in arrloc:
                        startpos = pos.end()
                        endpos = self.__brackets[(startpos-1,code[i][startpos-1])][0]
                        print(code[i][endpos])
                        code[i] = code[i][:startpos]+str(random.randint(10**9,10**11))+code[i][endpos:]
                        edit = 1
                        tempFileExceptions -= 1
                        noOfExc -=1
                        if not tempFileExceptions:
                            itr+=1
                            self.__fileWrite(code, "indexOut",itr)
                            tempFileExceptions = perFileExceptions
                        if not noOfExc:
                            itr+=1
                            self.__fileWrite(code, "indexOut", itr)
                            return
            if edit:
                itr+=1
                self.__fileWrite(code, "indexOut", itr)
                            
    
            
    def dividebyzero(self, codeSnip):
        for i in range(len(codeSnip)):
            isBalanced = self.__checkParanthesis(codeSnip[i])
            if(not isBalanced[0]):
                print("Error:" + isBalanced[-1])
                exit(1)
            else:
                print("Success: " + isBalanced[-1])
            print(self.__brackets)
            print(codeSnip[i])
            if 'cout' in codeSnip[i]:
                codeSnip[i] = '\tcout<<{}/0;\n'.format(i)
            print(codeSnip[i])
        return codeSnip

    def error_funcName(self, codeSnip):
        for i in range(len(codeSnip)):
            isBalanced = self.__checkParanthesis(codeSnip[i])
            if(not isBalanced[0]):
                print("Error:" + isBalanced[-1])
                exit(1)
            else:
                print("Success: " + isBalanced[-1])
            print(self.__brackets)
            print(codeSnip[i])
            locFunc = re.finditer('[a-zA-Z_][a-zA-Z0-9_]*\(', codeSnip[i])
            for pos in locFunc:
                codeSnip[i] = codeSnip[i][:pos.start()]+codeSnip[i][pos.start():pos.end()].swapcase()+codeSnip[i][pos.end():]
            print(codeSnip[i])
        return codeSnip
    
    def induceArrayOutOfRange(self,codeSnip):
        self.__searchKeyword(codeSnip)
        isBalanced = self.__checkParanthesis(codeSnip)
        # print(self.__dataMap)
        if(not isBalanced[0]):
            print("Error:" + isBalanced[-1])
            exit(1)
        else:
            print("Success: " + isBalanced[-1])
        validarr = re.finditer('[a-zA-Z_][a-zA-Z0-9_]*\[',codeSnip)
        tempSnip = codeSnip
        for i in validarr:
            start = i.start()
            end=  self.__brackets[(i.end()-1,codeSnip[i.end()-1])][0]
            l = 0
            for s,e in self.__wordMap:
                if start >= s and start < e:
                    l=1
                    break
            if l:
                continue
            
            # print(codeSnip[start:end+1])
            
            tempSnip = tempSnip.replace(codeSnip[start:end+1],codeSnip[start:i.end()]+str(random.randint(10**9,10**11))+codeSnip[end])
            
        codeSnip = tempSnip
        
        return codeSnip
            
            
        
            
            

exc = ExceptionInducer()
exc.fileOpen('../../test_codes/test_add.cpp')
exc.indexExc(1)
