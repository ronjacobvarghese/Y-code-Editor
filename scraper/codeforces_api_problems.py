import requests
import bs4
import csv
import json
import time


PROBLEMS_TAG = "implementation"

url = 'https://codeforces.com/api/problemset.problems?tags={}'.format(
    PROBLEMS_TAG)
res = requests.get(url)

problemsCount = 0

try:
    res.raise_for_status()
except Exception as exc:
    print("There was a problem: {}".format(exc))

soup = bs4.BeautifulSoup(res.text, "html.parser")

responseJson = json.loads(str(soup))

problemsDictionary = responseJson['result']['problems']


print(problemsDictionary[1])

for r in problemsDictionary:
    problemsCount += 1
    if r['index'] in ['A','B','C']:
      with open('codeforces/problemset.csv', 'a+', encoding='utf-8', newline='') as f:
          f.write("{},{},{}\n".format(r['contestId'], r['index'], r['name']))

print(f'The no of problems:{problemsCount}')
