import random
import re

class ExceptionInducer:
    
    def __init__(self,noOfExc = 1):
        self.noOfExc = noOfExc

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
        self.__dataMap = []
        # print(codeSnip)
        searchDatatype = re.finditer('((\(|\s)+(int|char|bool|float)|^(int|char|bool|float))\s+',codeSnip)
        # print(list(searchDatatype))
        for i in searchDatatype:
            end = i.end()
            while codeSnip[end] != ";":
                end+=1
            # print(codeSnip[i.end():end])
            self.__dataMap.append((i.end(),end))
                                    
    def sqrtExc(self, codeSnip): 
        isBalanced = self.__checkParanthesis(codeSnip)
        if(not isBalanced[0]):
            print("Error:" + isBalanced[-1])
            exit(1)
        else:
            print("Success: " + isBalanced[-1])
        print(self.__brackets)
        locSqrt = re.finditer('sqrt\(', codeSnip)
        tempSnip = codeSnip
        for code in locSqrt:
            startPos = code.start()
            endPos = self.__brackets[(startPos+4,codeSnip[startPos+4])][0]+1
            tempSnip = tempSnip.replace(codeSnip[startPos:endPos],'sqrt({})'.format(random.randrange(-999999999,-1)))
            # print(tempSnip[startPos:endPos])

        return tempSnip

    def indexExc(self, codeSnip):
        for i in range(len(codeSnip)):
            isBalanced = self.__checkParanthesis(codeSnip[i])
            if(not isBalanced[0]):
                print("Error:" + isBalanced[-1])
                exit(1)
            else:
                print("Success: " + isBalanced[-1])
            print(self.__brackets)
            print(codeSnip[i])
            validtype = True
            for datatype in ['int','char','float','bool']:
                if datatype in codeSnip[i]:
                    validtype = False
            # validtype = re.search('(\s+(int|char|bool|float)|^(int|char|bool|float))\s+',codeSnip[i])
            validarr = re.search('[a-zA-Z_][a-zA-Z0-9_]*\[',codeSnip[i])
            if validtype and validarr:
                arrloc = re.finditer('[a-zA-Z_][a-zA-Z0-9_]*\[',codeSnip[i])
                for pos in arrloc:
                    startpos = pos.end()
                    endpos = self.__brackets[(startpos-1,codeSnip[i][startpos-1])][0]
                    print(codeSnip[i][endpos])
                    codeSnip[i] = codeSnip[i][:startpos]+str(random.randint(10**9,10**11))+codeSnip[i][endpos:]
                print(codeSnip[i])

        return codeSnip
    
            
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
            for s,e in self.__dataMap:
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
with open('testcode3.cpp', 'r+') as rfile:
    exc = ExceptionInducer()
    code = rfile.read()
    codeSnip = exc.induceArrayOutOfRange(code)
    with open('newtestcode3.cpp','w+') as wfile:
        wfile.write(codeSnip)

# with open('testcode3.cpp','r+') as rfile:
#     code = rfile.readlines()
#     codeSnip = exc.indexExc(code)
#     with open('newtestcode3.cpp','w+') as wfile:
#         for i in codeSnip:
#             wfile.write(i)

# with open('add.cpp','r+') as rfile:
#     code = rfile.readlines()
#     codeSnip = exc.dividebyzero(code)
#     with open('add2.cpp','w+') as wfile:
#         for i in codeSnip:
#             wfile.write(i)
    
# with open('testcode3.cpp','r+') as rfile:
#     code = rfile.readlines()
#     codeSnip = exc.error_funcName(code)
#     with open('newtestcode3.cpp','w+') as wfile:
#         for i in codeSnip:
#             wfile.write(i)