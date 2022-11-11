import csv
import os
import datetime
from prettytable import PrettyTable, ALL

class DataSet:
    def __init__(self, file_name):
        self.file_name=file_name
        self.vacancies_objects=[Vacancy(vac) for vac in self.csv_filer(*self.csv_reader(file_name))]

    def csv_reader(self,file):
        listFile = []
        with open(file, encoding='utf-8-sig') as File:
            reader = csv.reader(File, delimiter=',')
            for row in reader:
                listFile.append(row)
        return listFile[1:], listFile[0]

    def csv_filer(self,reader, list_naming):
        listFile = []
        for item in reader:
            if item.count('') == 0 and len(item) == len(list_naming):
                listFile.append(item)
        allVacancies = []
        for i in range(len(listFile)):
            vacancy = {}
            for j in range(len(list_naming)):
                name = list_naming[j]
                data = listFile[i][j]
                while data.find('<') > -1:
                    index1 = data.find('<')
                    index2 = data.find('>')
                    data = data[:index1] + data[index2 + 1:]
                if '\n' not in data:
                    data = " ".join(data.split())
                vacancy[name] = data
            allVacancies.append(vacancy)
        return allVacancies

class Vacancy:
    def __init__(self,vacancy_dict):
        self.name=vacancy_dict['name']
        self.description=vacancy_dict['description']
        self.key_skills=vacancy_dict['key_skills'].split('\n')
        self.experience_id=vacancy_dict['experience_id']
        self.premium=vacancy_dict['premium']
        self.employer_name=vacancy_dict['employer_name']
        self.salary=Salary(vacancy_dict['salary_from'], vacancy_dict['salary_to'], vacancy_dict['salary_gross'], vacancy_dict['salary_currency'])
        self.area_name=vacancy_dict['area_name']
        self.published_at=vacancy_dict['published_at']

class Salary:
    def __init__(self,salary_from,salary_to,salary_gross,salary_currency):
        self.salary_from=salary_from
        self.salary_to=salary_to
        self.salary_gross=salary_gross
        self.salary_currency=salary_currency

    def toRub(self, salary):
        return salary * currency_to_rub[self.salary_currency]

class InputConect:
    def __init__(self, filterParametr, sortParametr, isReversedSort, interval, collumns):
        self.filterParametr = filterParametr
        self.sortParametr = sortParametr
        self.isReversedSort = isReversedSort
        self.interval = interval
        self.collumns = collumns

    def parametrCheck(self):
        if ': ' not in self.filterParametr and self.filterParametr != '':
            print('Формат ввода некорректен')
            exit()
        self.filterParametr = self.filterParametr.split(': ')
        if len(self.filterParametr) == 2 and self.filterParametr[0] not in list(dictionary.values()):
            print('Параметр поиска некорректен')
            exit()
        if self.sortParametr not in list(dictionary.values()) and self.sortParametr != '':
            print('Параметр сортировки некорректен')
            exit()
        elif self.isReversedSort not in ['Да', 'Нет', '']:
            print('Порядок сортировки задан некорректно')
            exit()
        self.isReversedSort=(self.isReversedSort=='Да')
        if len(self.collumns) != 0:
            self.collumns = self.collumns.split(', ')
            self.collumns.insert(0, '№')

    def print_table(self, vacancies):
        self.interval.append(len(vacancies) + 1)
        allVacanciesList = vacancies if len(self.filterParametr) != 2 else filterTable(vacancies,self.filterParametr)
        if len(allVacanciesList) == 0:
            print('Ничего не найдено')
            return
        if type(allVacanciesList) is str:
            print(allVacanciesList)
            return
        allVacanciesList = allVacanciesList if len(self.sortParametr) == 0 else sortTable(allVacanciesList,self.sortParametr,self.isReversedSort)
        columns = list(reverse_dictionary.keys())[:-1]
        columns.insert(0, '№')
        table = PrettyTable(columns)
        table.hrules = ALL
        for i in range(len(allVacanciesList)):
            newVacancy = formatter(allVacanciesList[i])
            newVacancy = list(map(lambda x: f'{x[:100]}...' if len(x) > 100 else x, newVacancy))
            newVacancy.insert(0, i + 1)
            table.add_row(newVacancy)
        table.align = 'l'
        table.max_width = 20
        if len(self.interval) < 2 and len(self.collumns) < 2:
            print(table)
        elif len(self.interval) < 2:
            print(table.get_string(fields=self.collumns))
        elif len(self.interval) < 2:
            print(table.get_string(start=self.interval[0] - 1, end=self.interval[1] - 1))
        else:
            print(table.get_string(start=self.interval[0] - 1, end=self.interval[1] - 1, fields=self.collumns))

dictionary={'name':'Название',
            'description':'Описание',
            'key_skills':'Навыки',
            'experience_id':'Опыт работы',
            'premium':'Премиум-вакансия',
            'employer_name':'Компания',
            'salary_from':'Нижняя граница вилки оклада',
            'salary_to':'Верхняя граница вилки оклада',
            'salary_gross':'Оклад указан до вычета налогов',
            'salary_currency':'Идентификатор валюты оклада',
            'area_name':'Название региона',
            'published_at':'Дата публикации вакансии',
            'Оклад':'Оклад'}


workExperience={"noExperience": "Нет опыта",
        "between1And3": "От 1 года до 3 лет",
        "between3And6": "От 3 до 6 лет",
        "moreThan6": "Более 6 лет"}

weights_experience={"noExperience":0,
    "between1And3":1,
    "between3And6":2,
    "moreThan6":3}


currency={"AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум"}

boolTranslation={ 'True':'Да',
                  'TRUE':'Да',
                  'False':'Нет',
                  'FALSE':'Нет'}

reverse_dictionary = {"Название": "name",
    "Описание": "description",
    "Навыки": "key_skills",
    "Опыт работы": "experience_id",
    "Премиум-вакансия": "premium",
    "Компания": "employer_name",
    "Оклад":"Оклад",
    "Название региона": "area_name",
    "Дата публикации вакансии": "published_at",
    "Идентификатор валюты оклада": "salary_currency"}

currency_to_rub = {
    "AZN": 35.68,
    "BYR": 23.91,
    "EUR": 59.90,
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
    "RUR": 1,
    "UAH": 1.64,
    "USD": 60.66,
    "UZS": 0.0055,
}

def formatter(row : Vacancy):
    def check_data (date):
        date = date[:date.find('T')].split('-')
        return '.'.join(reversed(date))
    def check_end_field (salary):
        salary_from = int(float(salary.salary_from))
        salary_to = int(float(salary.salary_to))
        salary_from = f'{salary_from // 1000} {str(salary_from)[-3:]}' if salary_from > 1000 else salary_from
        salary_to = f'{salary_to // 1000} {str(salary_to)[-3:]}' if salary_to > 1000 else salary_to
        grossInformation = 'Без вычета налогов' if boolTranslation[salary.salary_gross] == 'Да' else 'С вычетом налогов'
        return f'{salary_from} - {salary_to} ({currency[salary.salary_currency]}) ({grossInformation})'
    return [row.name, row.description, '\n'.join(row.key_skills), workExperience[row.experience_id],
               boolTranslation[row.premium], row.employer_name, check_end_field(row.salary), row.area_name,
               check_data(row.published_at)]

def filterTable(data_vacancies: list,parametr):
    columnName = parametr[0]
    data = parametr[1]
    if columnName=='Оклад':
        return list(filter(lambda vacancy: int(vacancy.salary.salary_from) <= int(data) <= int(vacancy.salary.salary_to), data_vacancies))
    elif columnName=='Навыки':
        data = data.split(', ')
        return list(filter(lambda vacancy: all(skill in vacancy.key_skills for skill in data), data_vacancies))
    elif columnName=='Опыт работы':
        return list(filter(lambda vacancy: data==workExperience[vacancy.__getattribute__(reverse_dictionary[columnName])], data_vacancies))
    elif columnName=='Дата публикации вакансии':
        return list(filter(lambda  vacancy: data==datetime.datetime.strptime(vacancy.published_at, '%Y-%m-%dT%H:%M:%S%z').strftime('%d.%m.%Y'), data_vacancies))
    elif columnName == 'Идентификатор валюты оклада':
        return list(filter(lambda vacancy: data==currency[vacancy.salary.salary_currency], data_vacancies))
    elif columnName == 'Премиум-вакансия':
        return list(filter(lambda vacancy: data==boolTranslation[vacancy.__getattribute__(reverse_dictionary[columnName])], data_vacancies))
    else:
        return list(filter(lambda vacancy: data==vacancy.__getattribute__(reverse_dictionary[columnName]),data_vacancies))

def sortTable(data_vacancies,parametr, isReversedSort):
    if parametr=='Навыки':
        data_vacancies.sort(key=lambda vacancy: len(vacancy.key_skills), reverse=isReversedSort)
    elif parametr=='Оклад':
        data_vacancies.sort(key=lambda vac: vac.salary.toRub(float(vac.salary.salary_from) + float(vac.salary.salary_to))/2, reverse=isReversedSort)
    elif parametr=='Дата публикации вакансии':
        data_vacancies.sort(key=lambda vac: datetime.datetime.strptime(vac.published_at,'%Y-%m-%dT%H:%M:%S%z'), reverse=isReversedSort)
    elif parametr=='Опыт работы':
        data_vacancies.sort(key=lambda vacancy: weights_experience[vacancy.experience_id], reverse=isReversedSort)
    else:
        data_vacancies.sort(key=lambda vacancy : vacancy.__getattribute__(reverse_dictionary[parametr]), reverse=isReversedSort)
    return data_vacancies

def input_data():
    file = input('Введите название файла: ')
    parametrOfFiltr = input('Введите параметр фильтрации: ')
    parametrOfSort = input('Введите параметр сортировки: ')
    isReversedSort = input('Обратный порядок сортировки (Да / Нет): ')
    rowsNumbers = list(map(int, input('Введите диапазон вывода: ').split()))
    collomnNames = input('Введите требуемые столбцы: ')
    if os.stat(file).st_size == 0:
        print("Пустой файл")
        exit()
    outer = InputConect(parametrOfFiltr, parametrOfSort, isReversedSort, rowsNumbers,collomnNames)
    outer.parametrCheck()
    dataset = DataSet(file)
    if len(dataset.vacancies_objects)==0:
        print('Нет данных')
        exit()
    outer.print_table(dataset.vacancies_objects)

input_data()
