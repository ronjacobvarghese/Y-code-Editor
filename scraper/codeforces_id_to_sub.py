import requests, bs4, csv, time


CATEGORIES = ['OK','CE','OTHR','WA']

for cat in CATEGORIES:
    i = 0

    with open('../codeforces/submission_ids_{}.csv'.format(cat),'r',encoding='utf-8', newline='') as r:
        
        reader = csv.reader(r)
        
        with open('../codeforces/submissions/code_snippets_2_{}.csv'.format(cat),'w',encoding='utf-8', newline = '') as w:

            writer = csv.writer(w)
            
            for row in reader:
                print(row)
                try:
                    PROBLEM_NUMBER = row[0]
                    PROBLEM_LETTER = row[1]
                    PROBLEM_NAME = row[2]
                    SUBMISSION_ID = row[3]
                    VERDICT = row[4]
                    TIME = row[5]
                    MEMORY = row[6]
                    
                    l = 1;r = 0
                    while l and r < 20:
                        time.sleep(1)
                        res = requests.get('http://codeforces.com/contest/{}/submission/{}'.format(PROBLEM_NUMBER,SUBMISSION_ID),timeout = 10)
                        #check if the download succeeded 
                        try:
                            res.raise_for_status()
                        except Exception as exc:
                            print('There was a problem: {}'.format(exc))
                
                        #turn the context (res.text) into a BeautifulSoup object
                        site_content = bs4.BeautifulSoup(res.text,"html.parser")
            
                        #actual submission inside denoted by the <pre class="prettyprint program-source".
                        elems = site_content.find("pre", { "id" : "program-source-text" })
                        if elems:
                            l = 0
                        else:
                            r+=1
                        print(r,end = '')
                    print()
                            
                    if r == 20:
                        time.sleep(600)
                        with open("../codeforces/submissions/code_snippets_incomplete.csv","+a", encoding = "utf-8",newline = '') as f:
                            f.write(f"{PROBLEM_NUMBER},{PROBLEM_LETTER},{SUBMISSION_ID},{PROBLEM_NAME},{TIME},{MEMORY}\n")
                        continue
                
                    print(elems)

                    print('got {} submission: {} problem number: {} problem_letter: {} submission_id: {}'.format(cat,i,PROBLEM_NUMBER,PROBLEM_LETTER,SUBMISSION_ID))
                    i += 1
                    
                    writer.writerow([PROBLEM_NUMBER,PROBLEM_LETTER,'{} '.format(elems.getText()),VERDICT,TIME,MEMORY])
                except AttributeError as err:
                    print(f"We got a problem: {err}")
                    with open("../codeforces/submissions/code_snippets_incomplete.csv","+a", encoding = "utf-8",newline = '') as f:
                        f.write(f"{PROBLEM_NUMBER},{PROBLEM_LETTER},{SUBMISSION_ID},{PROBLEM_NAME},{TIME},{MEMORY}\n")
                    continue
print('DONE!')