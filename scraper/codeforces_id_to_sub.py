import requests, bs4, csv



with open('../codeforces/problemset_completed.csv','r',encoding = 'utf-8',newline = '') as f:
    readFile = csv.reader(f)
    
    for row in readFile:
        PROBLEM_NUMBER = '282'
        PROBLEM_LETTER = 'A'

        categories = ['CE','OK','OTHR','WA']

        for cat in categories:
            i = 0

            with open('codeforces/{}{}_GNUC/submission_ids_{}_{}{}GNUC.csv'.format(PROBLEM_NUMBER,PROBLEM_LETTER,cat,PROBLEM_NUMBER,PROBLEM_LETTER),'r',encoding='utf-8', newline='') as r:
                
                reader = csv.reader(r)
                
                with open('codeforces/{}{}_GNUC/submissions_{}_{}{}GNUC.csv'.format(PROBLEM_NUMBER,PROBLEM_LETTER,cat,PROBLEM_NUMBER,PROBLEM_LETTER),'w',encoding='utf-8', newline = '') as w:

                    writer = csv.writer(w)
                    
                    for row in reader:
                        
                        res = requests.get('http://codeforces.com/contest/{}/submission/{}'.format(PROBLEM_NUMBER,row[0]))

                        #check if the download succeeded 
                        try:
                            res.raise_for_status()
                        except Exception as exc:
                            print('There was a problem: {}'.format(exc))
                
                        #turn the context (res.text) into a BeautifulSoup object
                        site_content = bs4.BeautifulSoup(res.text,"html.parser")
            
                        #actual submission inside denoted by the <pre class="prettyprint program-source".
                        elems = site_content.find_all("pre", { "class" : "prettyprint lang-c program-source" })

                        print('got {} submission: {}'.format(cat,i))
                        i += 1
                        
                        writer.writerow(['<START> {} <END>'.format(elems[0].getText()),row[1]])
        print('DONE!')
    
