import csv

frekwencja = []

with open('frekwencja_gminy.csv', 'r', encoding='utf-8-sig') as csvfile:
    freader = csv.reader(csvfile, dialect='excel', delimiter=';')
    for row in freader:
        frekwencja.append(row)

for i in range(1,5):
    print(frekwencja[i])
