import csv
import re

csv_fileName = input()
with open(csv_fileName, encoding='utf-8-sig') as r_file:
    csv_file = csv.reader(r_file)
    flag = False
    vacancies = []
    name_vacancies = []

    for line in csv_file:
        if flag == False:
            name_vacancies = line
        else:
            flag2 = True
            if '' in line:
                flag2 = False
                continue
            if len(line) == len(name_vacancies):
                data = []
                for i in line:
                    if '\n' in i:
                        i = i.replace('\n', ', ')
                    clean = re.sub(r'<.*?>', '', i)
                    clean = re.sub(r'\s+', ' ', ''.join(clean)).strip()
                    data.append(clean)

                if flag2:
                    vacancies.append(data)
        flag = True;

for j in range(0, len(vacancies)):
    for i in range(0, len(name_vacancies)):
        print(name_vacancies[i] + ': ' + vacancies[j][i])
        if i == len(name_vacancies) - 1:
           print()