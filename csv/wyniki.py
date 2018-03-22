import csv

with open('gm-okr01.csv', 'r', encoding='utf-8') as csvfile:
    freader = csv.reader(csvfile, dialect='excel', delimiter=',')
    wyniki = [row for row in freader]

for i in range(5):
    print(wyniki[i])
