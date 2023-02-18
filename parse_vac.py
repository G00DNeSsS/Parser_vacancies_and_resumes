import csv
import requests, random
from bs4 import BeautifulSoup
import config
import json as js
from colorama import Fore
import datetime
import PySimpleGUI as sg
import time
from threading import Thread
import re


        
proxies = {
    'http': 'http://64.74.163.147:11755',
    'htts': 'https://64.74.163.147:11755',
}

auth = ('kakamar3787','8ac388')
dateTimeObj = datetime.datetime.now()
timestampStr = dateTimeObj.strftime("%H:%M:%S")


def transliterate(name):
   # Слоаврь с заменами
   slovar = {
    ' ': '+'
	}
        
   # Циклически заменяем все буквы в строке
   for key in slovar:
      name = name.replace(key, slovar[key])
   return name

def translite_region(name):
   # Слоаврь с заменами
   slovar = {
    'СПБ': '2',
    'МСК': '1'
	}
        
   # Циклически заменяем все буквы в строке
   for key in slovar:
      name = name.replace(key, slovar[key])  
   return name	

area = config.HEADHUNTER_AREA_PARAM



def init(name, page, salary, checkbox,region,education, exp,employment,work_time):
	region_text = translite_region(region)
	text_work = name
	text_work_rus=text_work
	text_work=transliterate(text_work)
	profession = text_work
	pages = page
	d = {
		"prof": profession,
		"pages" : pages,
		"text_work_rus": text_work_rus,
		"salary" : salary,
		"Checkbox" : checkbox,
		"area" : region_text,
		"education" : education,
		"exp": exp,
		"employment" : employment,
		"work_time" : work_time
	}
	return d
		

def get_response(dict):
	content_links=[]
	URL = 'https://hh.ru/search/vacancy?'
	if dict["prof"]:
		URL = URL + "text=" +dict["prof"]
	if dict["salary"]:
		URL = URL + "&salary="+ dict["salary"]
	if dict["Checkbox"] == True:
		URL = URL + "&only_with_salary=true"
	if dict["Checkbox"] == False:
		URL = URL + "&only_with_salary=false"
	for item in dict['area']:
		if item == "2":
			URL = URL + "&area=2"	
		if item == "1":
			URL = URL + "&area=1"
	if dict["education"]:
		if dict["education"] == "Не требуется или не указано":
			URL = URL + "&education=not_required_or_not_specified"	
		if dict["education"] == "Высшее":
			URL = URL + "&education=higher"
		if dict["education"] == "Среднее профессиональное":
			URL = URL + "&education=special_secondary"
	if dict["exp"]:
		if dict["exp"] == "Не имеет значение":
			URL = URL
		if dict["exp"] == "От 1 до года до 3 лет":
			URL = URL + "&experience=between1And3"
		if dict["exp"] == "От 3 до 6 лет":
			URL = URL + "&experience=between3And6"
		if dict["exp"] == "Нет опыта":
			URL = URL + "&experience=noExperience"
		if dict["exp"] == "Больше 6 лет":
			URL = URL + "&experience=moreThan6"
	if dict["employment"]:
		if dict["employment"] == "Полная занятость":
			URL = URL + "&employment=full"
		if dict["employment"] == "Частичная занятость":
			URL = URL + "&employment=part"
		if dict["employment"] == "Проектная работа":
			URL = URL + "&employment=project"
		if dict["employment"] == "Стажировка":
			URL = URL + "&employment=probation"
		if dict["employment"] == "Волонтерство":
			URL = URL + "&employment=volunteer"
	if dict["work_time"]:
		if dict["work_time"] == "Полный день":
			URL = URL + "&schedule=fullDay"
		if dict["work_time"] == "Сменный график":
			URL = URL + "&schedule=shift"
		if dict["work_time"] == "Гибкий график":
			URL = URL + "&schedule=flexible"
		if dict["work_time"] == "Удаленная работа":
			URL = URL + "&schedule=remote"
		if dict["work_time"] == "Вахтовый метод":
			URL = URL + "&schedule=flyInFlyOut"
	for pag in range(int(dict['pages'])):
		URL_main =  URL +"&page="+str(pag)+"&hhtmFrom=vacancy_search_list"
		print(URL_main)
		content_links.append({
			"link": URL_main
		})	
	return content_links


def get_page_content(content_links,dict):
	'''Поиск всех данных на одной конкретной page'''
	content = []
	content1 = []
	for response_links in content_links:
		response = requests.get(
			response_links["link"], headers=config.HEADERS)
		soup = BeautifulSoup(response.text, "html.parser")
		vacancies = soup.find_all("div", class_="vacancy-serp-item__layout")
		if len(vacancies) == 0:
			continue
		else:
			for vac in vacancies:
				content.append(
					{
						"link" : vac.find('a', attrs={'class' : 'serp-item__title', 'data-qa': 'serp-item__title', 'target':'_blank'}).get("href")
					}
				)
	for i in content:
		responce = requests.get(i["link"], headers=config.HEADERS, proxies=proxies, auth=auth,  timeout=10)
		soup1 = BeautifulSoup(responce.text, "html.parser")
		vacancies1 = soup1.find_all("div", attrs={'id':'HH-React-Root'})
		if len(vacancies1) == 0:
			continue
		else:
			for result in vacancies1:

				name = result.find('h1',attrs={'class' : 'bloko-header-section-1', 'data-qa': 'vacancy-title'})
				if name:
					name_text = name.get_text(strip=True)
				else:
					name_text = "Должность не указана"
					

				cash = result.find('div',attrs={'data-qa': 'vacancy-salary'})
				if cash:
					cash_text = cash.get_text(strip=True)	
				else:
					cash_text = "Зарплата не указана"

				experience_count = result.find('span',	attrs={'data-qa' : 'vacancy-experience'})
				if experience_count:
					experience_count_text = experience_count.get_text(strip=True)	
				else:
					experience_count_text = "Опыт не указан"

				company_name = result.find('span',attrs={'class': 'vacancy-company-name'})	
				if company_name:
					company_name_text = company_name.get_text(strip=True)	
				else:
					company_name_text = "Компания не указана"
					
				address = result.find('span',attrs={'data-qa': 'vacancy-view-raw-address'})	
				if address:
					address_text = address.get_text(strip=True)
				else:
					address_text = "Адрес не указан"

				employment = result.find('p',attrs={'data-qa': 'vacancy-view-employment-mode', 'class': 'vacancy-description-list-item'})
				if employment:
					employment_text = employment.get_text(strip=True)
				else:
					employment_text = "Тип занятости не указан"
				
				description = result.find('div',attrs={'class' : 'g-user-content','data-qa': 'vacancy-description'})
				if description:
					description_text = description.get_text(strip=True)
				else:
					description = result.find('div',attrs={'class' : 'vacancy-branded-user-content', 'itemprop' : 'description' ,'data-qa': 'vacancy-description'})
					if description:
						description_text = description.get_text(strip=True)
					else:
						description_text = "Описание не указано"

				skills = result.find('div',attrs={'class' : 'bloko-tag-list'})
				if skills:
					skills_text = skills.get_text(strip=True)
				else:
					skills_text = "Не указано"

				result = skills_text[0]
				for letter in skills_text[1:]:
					if letter.isupper():
						result += f' {letter}'
					else:
						result += letter

				content1.append(
					{	
						"name" : name_text,
						"company_name": company_name_text,
						"cash": cash_text,
						"experience_count": experience_count_text,
						"description": description_text,
						"address" : address_text,
						"employment" : employment_text,
						"skills" : result,
						"link" : i["link"]
					}
				)			
	return content1
		
					
def write_in_file(data,dict):
	try:
		with open(f"{dict['text_work_rus'].title()}.{config.SAVE_FILE_EXTENSION}", "w", newline="",errors='ignore') as file:
			writer = csv.writer(file, delimiter=";")

			writer.writerow(["Должность", "Компания","Зарплата", "Опыт работы", "Описание","Адрес", "Тип занятости", "Ключевые навыки", "Ссылка"])

			for dataset in data:
				writer.writerow([dataset["name"], dataset["company_name"] ,dataset["cash"],dataset["experience_count"], dataset["description"], dataset["address"], dataset["employment"],dataset["skills"], dataset["link"]])

		print(f"{'Файл Вакансии -'+dict['text_work_rus'].title()}.{config.SAVE_FILE_EXTENSION} сохранён на рабочий стол!")
	except Exception as exc:
		print(str(exc))
		print("Ошибка при записи в файл.")

	
def make_array_from_list_of_dicts(list_of_dicts):
    return [[i for i in j.values()] for j in list_of_dicts]

def main_parse(resume, page, salary,checkbox,  region, education, exp, employment, work_time, dict_table,main_window):
	dict_1 = init(resume,page,salary,checkbox,region, education, exp,employment,work_time)
	responses = []
	responses.append(get_response(dict_1))
	data = []
	if get_page_content(responses[0],dict_1) == None:
		print("По вашему запросу ничего не найдено!")
	else:
		for resp in responses:
			content = get_page_content(resp,dict_1)
			if content != None:
				for dataset in content:
					data.append(dataset)	
			else:
				break
	
	dict_table = make_array_from_list_of_dicts(content)
	main_window['-TABLE-'].update(values=dict_table, visible=True)
	write_in_file(data,dict_1)

def make_window(theme=None):
	sg.theme(theme)
	headings = ["Должность", "Компания", "Зарплата", "Опыт работы", "Описание","Адрес", "Тип занятости", "Ключевые навыки", "Ссылка"]
	data_table = []
	#menu_def=['&File', ['&New File', '&Open...','Open &Module','---', '!&Recent Files','C&lose']],['&Save',['&Save File', 'Save &As','Save &Copy'  ]],['&Edit', ['&Cut', '&Copy', '&Paste']]
	layout = [ 
			#[sg.Menu(menu_def, key='-MENU-')],
			[sg.Button('Старт', button_color=('black','white'), key='Play'),sg.Button('Выход', button_color=('black','white'), key='-Stop-'), sg.Text('                                                                                                                                                                                   Тема:',justification='center'),sg.Combo(sg.theme_list(), default_value=sg.theme(), s=(15,22), enable_events=True, readonly=True, k='-Theme-')],
			[sg.HSep()],
			[sg.VSep(),sg.Text('Введите вакансию:'), sg.InputText(key='-VAC-',size=(40, 1)),sg.Text('Образование:'),sg.Combo(values=('Не требуется или не указано','Высшее', 'Среднее профессиональное'),  readonly=True, key='-COMBO-',expand_x=True),sg.VSep()],
			[sg.VSep(),sg.Text('Количество страниц (1 страница = 20 вакансий):'), sg.InputText(key='-PAGE-',size=(15, 1)),sg.Text('Опыт работы:'),sg.Combo(values=('Не имеет значения','От 1 до года до 3 лет', 'От 3 до 6 лет', 'Нет опыта', 'Больше 6 лет'), readonly=True, key='-COMBO_Exp-',expand_x=True),sg.VSep()],
			[sg.VSep(),sg.Text('Укажите регион(ы) через пробел:'), sg.InputText(key='-Region-',size=(28, 1)),sg.Text('График работы:'),sg.Combo(values=('Полный день','Сменный трафик', 'Гифкий график', 'Удаленная работа', 'Вахтовый метод'), readonly=True, key='-COMBO_time_work-',expand_x=True),sg.VSep()],
			[sg.VSep(),sg.Text('Укажите уровень дохода от:'), sg.InputText(key='-Salary-',size=(32, 1)),sg.Text('Тип занятости:'),sg.Combo(values=('Полная занятость','Частичная занятость', 'Проектная работа', 'Стажировка', 'Волонтерство'), readonly=True, key='-COMBO_employment-',expand_x=True),sg.VSep()],
			[sg.VSep(),sg.Text('Указан доход:'),sg.Checkbox('', default=False, key='-Checkbox-',expand_x=True),sg.VSep()],
			[sg.HSep()],
			[sg.Table(values=data_table, headings=headings,  visible = False,  vertical_scroll_only = False, max_col_width=40,
                    auto_size_columns=True,
		    		right_click_selects=True,
                    num_rows=20,
		    		expand_x=True,
					justification='center', key='-TABLE-',
					selected_row_colors='red on yellow', 
					enable_events=True)]]

	window = sg.Window('Вакансии HH.RU', layout,size=(1000, 600))

	return window


def parse():
	data_table = []
	window = make_window()	
	while True:
		event, values = window.read()
		if event == sg.WIN_CLOSED or event == '-Stop-': # if user closes window or clicks cancel
			break
		if values['-Theme-'] != sg.theme():
			sg.theme(values['-Theme-'])
			window.close()
			window = make_window()
		elif event == "Play":
			th = Thread(target=main_parse, args=(values['-VAC-'], values['-PAGE-'], values['-Salary-'], values['-Checkbox-'], values['-Region-'], values['-COMBO-'],values['-COMBO_Exp-'], values['-COMBO_employment-'], values['-COMBO_time_work-'], data_table,window))
			th.start()						
	window.close()

parse()	