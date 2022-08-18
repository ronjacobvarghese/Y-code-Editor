import requests
import bs4
import csv
import json
import time



with open('../codeforces/problemset_replica.csv', 'r', encoding ='utf-8', newline='') as r:
    readFile = csv.reader(r)

    with open('../codeforces/test_cases/test_cases.csv', 'w+', encoding='utf-8', newline='') as w:
        
        writeFile = csv.writer(w)
        
        for row in readFile:
            try:
              time.sleep(0.1)

              PROBLEM_NUMBER = row[0]
              PROBLEM_LETTER = row[1]
            
              res = requests.get('https://codeforces.com/contest/{}/problem/{}'.format(PROBLEM_NUMBER,PROBLEM_LETTER))
              
              try:
                res.raise_for_status()
              except Exception as exc:
                print("There was a problem: {}".formate(exc))
                
              site_content = bs4.BeautifulSoup(res.text,"html.parser")
              
              div_elem = site_content.find("div", { "class": "input" })
              print(div_elem.pre.getText())
              
              testCase = div_elem.pre.getText()

              writeFile.writerow([PROBLEM_NUMBER,PROBLEM_LETTER,testCase])
            except AttributeError as err:
              print('We have a problem: {}'.format(err))
              with open('../codeforces/test_cases/test_cases_incomplete.csv','a+',encoding='utf-8',newline = '') as f:
                f.write('{},{}\n'.format(PROBLEM_NUMBER,PROBLEM_LETTER))
              continue
              
print('DONE!!')
          