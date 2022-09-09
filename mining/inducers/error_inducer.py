import code
import re

    

class errors:

    def fileOpen(self,filename):
        with open (filename,'r',encoding='utf-8') as f:
            self.codeSnip = f.readlines()
            f.close()
            
    def __fileWrite__(self, errorSnip, error,no):
        with open(f'../../test_codes/E_test_{error}_{no}',"w",encoding='utf-8') as f:
            f.write("".join(errorSnip))
            f.close()
            


    def emptyLoop(self, perFileError = 10, noOfErr = 20):
        itr = 0;filePtr = 0
        n = len(self.codeSnip)
        while noOfErr and filePtr != n: 
            code = self.codeSnip.copy()
            a=["while","for"]
            edit = 0
            tempFileError = perFileError
            for i in range(filePtr,len(code)):
                filePtr = i+1
                # if "while" in code[i]:
                if any(x in code[i] for x in a):
                    edit = 1    
                    tmp = list(code[i])
                    
                    for j in range(len(tmp)):
                        if tmp[j]==")":
                            tmp=tmp[0:j+1]+[";"]+tmp[j+1:]
                            break
                    code.pop(i)
                    code.insert(i,"".join(tmp))
                    noOfErr -= 1
                    tempFileError -= 1
                if not tempFileError:
                    itr+=1
                    break
            if edit:
                self.__fileWrite__(code,"EmptyLoop",itr);
            
            
    
    def removeReturn(self,codeSnip,noOfErr = 2):
        codeSnip = codeSnip.readlines()
        pass
    

    def equalityComparisontoAssignment(self, perFileError = 10, noOfErr = 20):
        itr = 0;filePtr = 0
        n = len(self.codeSnip)
        while noOfErr and filePtr != n:
            for i in range(len(codesnip)):
                if "if" in codesnip[i]:
                    # tmp=list(codesnip[i])
                    # index=codesnip.find("==")
                    # print(index)
                    tmp=codesnip[i].split()
                    print(tmp)
                    for j in range(len(tmp)):
                        if "==" in tmp[j]:
                            index=tmp[j].find("==")
                            tmp[j]=tmp[j][:index]+tmp[j][index+1:]+'\n'        
                    codesnip.pop(i)
                    codesnip.insert(i," ".join(tmp))
                    t-=1
                if t==0:
                    return codesnip
            print("".join(codesnip))
            return codesnip
    
    # [+=,-=,/=,%=]
    def errors_in_assignment_operators(self,codesnip,t=2):
        a=["while","for"]
        c=["*=","/="]
        for i in range(len(codesnip)):
            if not any (x in codesnip[i] for x in a):
                if "=" in codesnip[i] and not "==" in codesnip[i] and not "//" in codesnip[i]:
                    print(i)
                    print("the codesnip is",codesnip[i],)
                    if any (y in codesnip[i] for y in c):
                        tmpr=list(codesnip[i])
                        index=tmpr.index("=")
                        tmpr.insert(index+1,tmpr[index-1])
                        tmpr.pop(index-1)
                        print("".join(tmpr))
                        codesnip.pop(i)
                        codesnip.insert(i,"".join(tmpr))
                        print(codesnip.index("".join(tmpr)))
                        t-=1
                    if t==0:
                        return codesnip
        print("".join(codesnip))
        return codesnip


    def left_assignment_to_right(self,codesnip,t=2):
        a=["while","for"]
        b=["+","-","*","/"]
        c=["+=","-=","*=","/="]
        for i in range(len(codesnip)):
            if not any (x in codesnip[i] for x in a):
                if "=" in codesnip[i] and not "==" in codesnip[i] and not "//" in codesnip[i]:
                    if not any (x in codesnip[i] for x in c):
                        print(i)
                        print("the codesnip is",codesnip[i],)
                        if any(x in codesnip[i] for x in b):
                            tmp=list(codesnip[i])
                            index = tmp.index("=")
                            index1 = tmp.index(";")
                            tmp1=tmp[index+1:index1]
                            tmp1.append("=")
                            print(tmp1)
                            for j in range(index):
                                tmp1.append(tmp[j])
                            tmp1.append(";\n")
                            print(tmp1)
                            tmp2=''.join(tmp1).replace(" ","")
                            print(tmp2)
                            codesnip.pop(i)
                            codesnip.insert(i,tmp2)
                            t-=1
                        if t==0:
                            return codesnip
        print("".join(codesnip))
        return codesnip
            

    def notypedeclaration(self,codesnip,t=2):
            a=["int","float","double","char","wchar_t","bool","string"]
            b=["main","for","="]
            # for i in range(len(codesnip)):
            #     if any(x in codesnip[i] for x in a):
            #         if not any(x in codesnip[i] for x in b):
            #             print(codesnip[i])
            for i in range(len(codesnip)):
                match=re.search("(int|char|bool|float|long|long Long|string)",codesnip[i])
                if match!=None:
                    startpos=match.start()
                    endpos=match.end()
                    codesnip[i]=codesnip[i][:startpos]+codesnip[i][endpos+1:]
                    print(codesnip[i])
                    t-=1
                if t==0:
                    return codesnip
            return codesnip
    
    def else_if_concatenate(self,codesnip,t=2):
        for i in range(len(codesnip)):
            if "else if" in codesnip[i]:
                print(codesnip[i])


Err = errors()
codesnip=Err.fileOpen("../../test_codes/test_add.cpp")
codesnip2=Err.emptyLoop(1)

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
