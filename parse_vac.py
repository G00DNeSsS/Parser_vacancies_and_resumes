import csv
import requests, random
from bs4 import BeautifulSoup
import config
import json
import json as js
from colorama import Fore
import datetime
import PySimpleGUI as sg
import time
from threading import Thread
import re
import statistics
import string
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pylab
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

        
proxies = {
    'http': 'http://64.74.163.147:11755',
    'htts': 'https://64.74.163.147:11755',
}

auth = ('kakamar3787','8ac388')


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

def init(name, page, salary, checkbox,region,education, exp,employment,work_time,val):
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
		"work_time" : work_time,
		"val" : val
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
	if dict["val"]:
		if dict["val"] == "RUB":
			URL = URL + "&currency_code=rub"
		if dict["val"] == "EUR":
			URL = URL + "&currency_code=EUR"
		if dict["val"] == "USD":
			URL = URL + "&currency_code=USD"
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
		responce = requests.get(i["link"], headers=config.HEADERS, timeout=10)
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


				city = result.find('span',attrs={'data-qa': 'vacancy-view-raw-address'})	
				if city:
					city_text = city.get_text(strip=True)
					head, sep, tail = city_text.partition(',')
					city_text = head
				else:
					city_text = "Город не указан"	
					
				address = result.find('span',attrs={'data-qa': 'vacancy-view-raw-address'})	
				if address:
					address_text = address.get_text(strip=True)
					head, sep, tail = address_text.partition(',')
					address_text = tail
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
						"city": city_text,
						"address" : address_text,
						"employment" : employment_text,
						"skills" : result,
						"link" : i["link"]
					}
				)
	with open('content.json', 'w', encoding='utf-8') as f:
		json.dump(content1, f, ensure_ascii=False, indent=4)					
	return content1
		
					
def write_in_file(data,dict):
	try:
		with open(f"{dict['text_work_rus'].title()}.{config.SAVE_FILE_EXTENSION}", "w", newline="",errors='ignore') as file:
			writer = csv.writer(file, delimiter=";")

			writer.writerow(["Должность", "Компания","Зарплата", "Опыт работы", "Описание","Город", "Адрес", "Тип занятости", "Ключевые навыки", "Ссылка"])

			for dataset in data:
				writer.writerow([dataset["name"], dataset["company_name"] ,dataset["cash"],dataset["experience_count"], dataset["description"], dataset["city"], dataset["address"], dataset["employment"],dataset["skills"], dataset["link"]])

		print(f"{'Файл Вакансии -'+dict['text_work_rus'].title()}.{config.SAVE_FILE_EXTENSION} сохранён на рабочий стол!")
	except Exception as exc:
		print(str(exc))
		print("Ошибка при записи в файл.")

	
def make_array_from_list_of_dicts(list_of_dicts):
    return [[i for i in j.values()] for j in list_of_dicts]

def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def main_parse(resume, page, salary,checkbox,  region, education, exp, employment, work_time, val, dict_table,main_window):
	dict_1 = init(resume,page,salary,checkbox,region, education, exp,employment,work_time,val)
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

	exp_no_age = 0
	exp_1_3=0
	exp_3_6=0
	exp_more_6=0			
	for i in data:
		if i['experience_count'] == "1–3 года":
			exp_1_3 = exp_1_3+1
		if i['experience_count'] == "3–6 лет":
			exp_3_6 = exp_3_6+1
		if i['experience_count'] == "более 6 лет":
			exp_more_6 = exp_more_6+1
		if i['experience_count'] == "не требуется":
			exp_no_age = exp_no_age+1
		
			

	
	
	labels = 'Нет опыта работы', '1 - 3 год', '3 - 6 год', 'Более 6 лет'
	sizes = [exp_no_age, exp_1_3, exp_3_6, exp_more_6]
	explode = (0.2, 0.2, 0.2, 0.2)
	fig1 = plt.figure(figsize=(15, 10))
	plt.title('Требуемый опыт работы (%)')
	plt.pie(sizes, autopct='%1.1f%%', shadow=True, explode=explode, wedgeprops={'lw':1, 'ls':'--','edgecolor':"k"})
	plt.legend(bbox_to_anchor = (0.15, 1.1),labels = labels)
	draw_figure(main_window['-CANVAS_circle-'].TKCanvas, fig1)
	plt.close()
	
	data_cash=[]
	data_cash_With_exp_more_6=[]
	data_cash_With_exp_1_3=[]
	data_cash_With_exp_3_6=[]

	for i in data:
		if i['cash'].find("руб")!= -1:
			int_rub_text=i['cash'].replace('\xa0','')
			head, sep, tail = int_rub_text.partition('руб')
			if head.find("от")!= -1:
				prom = head.replace('от','')
				if prom.find("до")!= -1:
					head, sep, tail = prom.partition('до')
					data_cash.append(int(head))
					continue
				else:
					data_cash.append(int(prom))
					continue
			if head.find("до")!= -1:
				prom = head.replace('до','')
				if prom.find("от")!= -1:
					head, sep, tail = prom.partition('от')
					data_cash.append(int(head))
					continue
				else:
					data_cash.append(int(prom))
					continue
		if i['cash'].find("USD")!= -1:
			int_usd_text=i['cash'].replace('\xa0','')
			head, sep, tail = int_usd_text.partition('USD')
			if head.find("от")!= -1:
				prom = head.replace('от','')
				if prom.find("до")!= -1:
					head, sep, tail = prom.partition('до')
					head = int(head) * 75.05
					data_cash.append(int(head))
					continue
				else:
					prom = int(prom) * 75.05
					data_cash.append(int(prom))
					continue	
			if head.find("до")!= -1:
				prom = head.replace('до','')
				if prom.find("от")!= -1:
					head, sep, tail = prom.partition('от')
					head = int(head) * 75.05
					data_cash.append(int(head))
					continue
				else:
					prom = int(prom) * 75.05
					data_cash.append(int(prom))
					continue
		if i['cash'].find("KZT")!= -1:
			int_kzt_text=i['cash'].replace('\xa0','')
			head, sep, tail = int_kzt_text.partition('KZT')
			if head.find("от")!= -1:
				prom = head.replace('от','')
				if prom.find("до")!= -1:
					head, sep, tail = prom.partition('до')
					head = int(head) * 0.17
					data_cash.append(int(head))
					continue
				else:
					prom = int(prom) * 0.17
					data_cash.append(int(prom))
					continue
			if head.find("до")!= -1:
				prom = head.replace('до','')
				if prom.find("от")!= -1:
					head, sep, tail = prom.partition('от')
					head = int(head) * 0.17							
					data_cash.append(int(head))
					continue
				else:
					prom = int(prom) * 0.17				
					data_cash.append(int(prom))
					continue
		if i['cash'].find("EUR")!= -1:
			int_kzt_text=i['cash'].replace('\xa0','')
			head, sep, tail = int_kzt_text.partition('EUR')
			if head.find("от")!= -1:
				prom = head.replace('от','')
				if prom.find("до")!= -1:
					head, sep, tail = prom.partition('до')
					head = int(head) * 80.37
					data_cash.append(int(head))
					continue
				else:
					prom = int(prom) * 80.37
					data_cash.append(int(prom))
					continue
			if head.find("до")!= -1:
				prom = head.replace('до','')
				if prom.find("от")!= -1:
					head, sep, tail = prom.partition('от')
					head = int(head) * 80.37
					data_cash.append(int(head))
					continue
				else:
					prom = int(prom) * 80.37
					data_cash.append(int(prom))
					continue
	data_cash = sorted(data_cash)
	median = statistics.median(data_cash)
	avg_cash = sum(data_cash)/len(data_cash)				
	for i in data:				
		if i['experience_count'] == "1–3 года":
			if i['cash'].find("руб")!= -1:
				int_rub_text=i['cash'].replace('\xa0','')
				head, sep, tail = int_rub_text.partition('руб')
				if head.find("от")!= -1:
					prom = head.replace('от','')
					if prom.find("до")!= -1:
						head, sep, tail = prom.partition('до')
						data_cash_With_exp_1_3.append(int(head))
						continue
					else:
						data_cash_With_exp_1_3.append(int(prom))
						continue
				
				if head.find("до")!= -1:
					prom = head.replace('до','')
					if prom.find("от")!= -1:
						head, sep, tail = prom.partition('от')
						data_cash_With_exp_1_3.append(int(head))
						continue
					else:
						data_cash_With_exp_1_3.append(int(prom))
						continue
				
			if i['cash'].find("USD")!= -1:
				int_usd_text=i['cash'].replace('\xa0','')
				head, sep, tail = int_usd_text.partition('USD')
				if head.find("от")!= -1:
					prom = head.replace('от','')
					if prom.find("до")!= -1:
						head, sep, tail = prom.partition('до')
						head = int(head) * 75.05
						data_cash_With_exp_1_3.append(int(head))
						continue
					else:
						prom = int(prom) * 75.05
						data_cash_With_exp_1_3.append(int(prom))
						continue
				
				if head.find("до")!= -1:
					prom = head.replace('до','')
					if prom.find("от")!= -1:
						head, sep, tail = prom.partition('от')
						head = int(head) * 75.05
						data_cash_With_exp_1_3.append(int(head))
						continue
					else:
						prom = int(prom) * 75.05
						data_cash_With_exp_1_3.append(int(prom))
						continue
				
			if i['cash'].find("KZT")!= -1:
				int_kzt_text=i['cash'].replace('\xa0','')
				head, sep, tail = int_kzt_text.partition('KZT')
				if head.find("от")!= -1:
					prom = head.replace('от','')
					if prom.find("до")!= -1:
						head, sep, tail = prom.partition('до')
						head = int(head) * 0.17
						data_cash_With_exp_1_3.append(int(head))
						continue
					else:
						prom = int(prom) * 0.17
						data_cash_With_exp_1_3.append(int(prom))
						continue
				
				if head.find("до")!= -1:
					prom = head.replace('до','')
					if prom.find("от")!= -1:
						head, sep, tail = prom.partition('от')
						head = int(head) * 0.17							
						data_cash_With_exp_1_3.append(int(head))
						continue
					else:
						prom = int(prom) * 0.17				
						data_cash_With_exp_1_3.append(int(prom))
						continue
				
			if i['cash'].find("EUR")!= -1:
				int_kzt_text=i['cash'].replace('\xa0','')
				head, sep, tail = int_kzt_text.partition('EUR')
				if head.find("от")!= -1:
					prom = head.replace('от','')
					if prom.find("до")!= -1:
						head, sep, tail = prom.partition('до')
						head = int(head) * 80.37
						data_cash_With_exp_1_3.append(int(head))
						continue
					else:
						prom = int(prom) * 80.37
						data_cash_With_exp_1_3.append(int(prom))
						continue
				
				if head.find("до")!= -1:
					prom = head.replace('до','')
					if prom.find("от")!= -1:
						head, sep, tail = prom.partition('от')
						head = int(head) * 80.37
						data_cash_With_exp_1_3.append(int(head))
						continue
					else:
						prom = int(prom) * 80.37
						data_cash_With_exp_1_3.append(int(prom))
						continue
		if i['experience_count'] == "3–6 лет":
			if i['cash'].find("руб")!= -1:
				int_rub_text=i['cash'].replace('\xa0','')
				head, sep, tail = int_rub_text.partition('руб')
				if head.find("от")!= -1:
					prom = head.replace('от','')
					if prom.find("до")!= -1:
						head, sep, tail = prom.partition('до')
						data_cash_With_exp_3_6.append(int(head))
						continue
					else:
						data_cash_With_exp_3_6.append(int(prom))
						continue
				
				if head.find("до")!= -1:
					prom = head.replace('до','')
					if prom.find("от")!= -1:
						head, sep, tail = prom.partition('от')
						data_cash_With_exp_3_6.append(int(head))
						continue
					else:
						data_cash_With_exp_3_6.append(int(prom))
						continue
					
			if i['cash'].find("USD")!= -1:
				int_usd_text=i['cash'].replace('\xa0','')
				head, sep, tail = int_usd_text.partition('USD')
				if head.find("от")!= -1:
					prom = head.replace('от','')
					if prom.find("до")!= -1:
						head, sep, tail = prom.partition('до')
						head = int(head) * 75.05
						data_cash_With_exp_3_6.append(int(head))
						continue
					else:
						prom = int(prom) * 75.05
						data_cash_With_exp_3_6.append(int(prom))
						continue
				
				if head.find("до")!= -1:
					prom = head.replace('до','')
					if prom.find("от")!= -1:
						head, sep, tail = prom.partition('от')
						head = int(head) * 75.05
						data_cash_With_exp_3_6.append(int(head))
						continue
					else:
						prom = int(prom) * 75.05
						data_cash_With_exp_3_6.append(int(prom))
						continue
						
			if i['cash'].find("KZT")!= -1:
				int_kzt_text=i['cash'].replace('\xa0','')
				head, sep, tail = int_kzt_text.partition('KZT')
				if head.find("от")!= -1:
					prom = head.replace('от','')
					if prom.find("до")!= -1:
						head, sep, tail = prom.partition('до')
						head = int(head) * 0.17
						data_cash_With_exp_3_6.append(int(head))
						continue
					else:
						prom = int(prom) * 0.17
						data_cash_With_exp_3_6.append(int(prom))
						continue
				
				if head.find("до")!= -1:
					prom = head.replace('до','')
					if prom.find("от")!= -1:
						head, sep, tail = prom.partition('от')
						head = int(head) * 0.17							
						data_cash_With_exp_3_6.append(int(head))
						continue
					else:
						prom = int(prom) * 0.17				
						data_cash_With_exp_3_6.append(int(prom))
						continue
					
			if i['cash'].find("EUR")!= -1:
				int_kzt_text=i['cash'].replace('\xa0','')
				head, sep, tail = int_kzt_text.partition('EUR')
				if head.find("от")!= -1:
					prom = head.replace('от','')
					if prom.find("до")!= -1:
						head, sep, tail = prom.partition('до')
						head = int(head) * 80.37
						data_cash_With_exp_3_6.append(int(head))
						continue
						
					else:
						prom = int(prom) * 80.37
						print(prom)
						data_cash_With_exp_3_6.append(int(prom))
						continue
				
				if head.find("до")!= -1:
					prom = head.replace('до','')
					if prom.find("от")!= -1:
						head, sep, tail = prom.partition('от')
						head = int(head) * 80.37
						data_cash_With_exp_3_6.append(int(head))
						continue
					else:
						prom = int(prom) * 80.37
						data_cash_With_exp_3_6.append(int(prom))	
						continue		
		if i['experience_count'] == "более 6 лет":
			if i['cash'].find("руб")!= -1:
				int_rub_text=i['cash'].replace('\xa0','')
				head, sep, tail = int_rub_text.partition('руб')
				if head.find("от")!= -1:
					prom = head.replace('от','')
					if prom.find("до")!= -1:
						head, sep, tail = prom.partition('до')
						data_cash_With_exp_more_6.append(int(head))
						continue
					else:
						data_cash_With_exp_more_6.append(int(prom))
						continue
				
				if head.find("до")!= -1:
					prom = head.replace('до','')
					if prom.find("от")!= -1:
						head, sep, tail = prom.partition('от')
						data_cash_With_exp_more_6.append(int(head))
						continue
					else:
						data_cash_With_exp_more_6.append(int(prom))
						continue
				
			if i['cash'].find("USD")!= -1:
				int_usd_text=i['cash'].replace('\xa0','')
				head, sep, tail = int_usd_text.partition('USD')
				if head.find("от")!= -1:
					prom = head.replace('от','')
					if prom.find("до")!= -1:
						head, sep, tail = prom.partition('до')
						head = int(head) * 75.05
						data_cash_With_exp_more_6.append(int(head))
						continue
					else:
						prom = int(prom) * 75.05
						data_cash_With_exp_more_6.append(int(prom))
						continue
				
				if head.find("до")!= -1:
					prom = head.replace('до','')
					if prom.find("от")!= -1:
						head, sep, tail = prom.partition('от')
						head = int(head) * 75.05
						data_cash_With_exp_more_6.append(int(head))
						continue
					else:
						prom = int(prom) * 75.05
						data_cash_With_exp_more_6.append(int(prom))
						continue
				
			if i['cash'].find("KZT")!= -1:
				int_kzt_text=i['cash'].replace('\xa0','')
				head, sep, tail = int_kzt_text.partition('KZT')
				if head.find("от")!= -1:
					prom = head.replace('от','')
					if prom.find("до")!= -1:
						head, sep, tail = prom.partition('до')
						head = int(head) * 0.17
						data_cash_With_exp_more_6.append(int(head))
						continue
					else:
						prom = int(prom) * 0.17
						data_cash_With_exp_more_6.append(int(prom))
						continue
				
				if head.find("до")!= -1:
					prom = head.replace('до','')
					if prom.find("от")!= -1:
						head, sep, tail = prom.partition('от')
						head = int(head) * 0.17							
						data_cash_With_exp_more_6.append(int(head))
						continue
					else:
						prom = int(prom) * 0.17				
						data_cash_With_exp_more_6.append(int(prom))
						continue
				
			if i['cash'].find("EUR")!= -1:
				int_kzt_text=i['cash'].replace('\xa0','')
				head, sep, tail = int_kzt_text.partition('EUR')
				if head.find("от")!= -1:
					prom = head.replace('от','')
					if prom.find("до")!= -1:
						head, sep, tail = prom.partition('до')
						head = int(head) * 80.37
						data_cash_With_exp_more_6.append(int(head))
						continue
					else:
						prom = int(prom) * 80.37
						print(prom)
						data_cash_With_exp_more_6.append(int(prom))
						continue
				
				if head.find("до")!= -1:
					prom = head.replace('до','')
					if prom.find("от")!= -1:
						head, sep, tail = prom.partition('от')
						head = int(head) * 80.37
						data_cash_With_exp_more_6.append(int(head))
						continue
					else:
						prom = int(prom) * 80.37
						data_cash_With_exp_more_6.append(int(prom))
						continue
							
		
	try:
		avg_more_6_cash = sum(data_cash_With_exp_more_6)/len(data_cash_With_exp_more_6)
	except ZeroDivisionError:
		avg_more_6_cash = 0
	try:
		avg_1_3_cash = sum(data_cash_With_exp_1_3)/len(data_cash_With_exp_1_3)
	except ZeroDivisionError:
		avg_1_3_cash = 0
	try:
		avg_3_6_cash = sum(data_cash_With_exp_3_6)/len(data_cash_With_exp_3_6)
	except ZeroDivisionError:
		avg_3_6_cash = 0


	data_exp = {
		"1 - 3 года" : int(avg_1_3_cash),
		"3 - 6 лет" : int(avg_3_6_cash),
		"Более 6 лет" : int(avg_more_6_cash)
	}
	plt.figure(figsize=(5.5, 5))
	courses = list(data_exp.keys())
	values = list(data_exp.values())
	barlot = plt.bar(courses, values, color ='blue', width = 0.3)
	plt.bar_label(barlot,labels=values,label_type='edge')
	plt.title("Средняя зарплата к опыту работы")	
	fig = plt.gcf()    
	draw_figure(main_window['-CANVAS-'].TKCanvas, fig)
	figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
	plt.close()

	cash_msk = []
	cash_spb = []
	cash_kazan = []
	cash_ekb = []
	cash_region = []

	for i in data:
		try:
			if i['city'] == "Москва":
				if i['cash'].find("руб")!= -1:
					int_rub_text=i['cash'].replace('\xa0','')
					head, sep, tail = int_rub_text.partition('руб')
					if head.find("от")!= -1:
						prom = head.replace('от','')
						if prom.find("до")!= -1:
							head, sep, tail = prom.partition('до')
							cash_msk.append(int(head))
							continue
						else:
							cash_msk.append(int(prom))
							continue
					if head.find("до")!= -1:
						prom = head.replace('до','')
						if prom.find("от")!= -1:
							head, sep, tail = prom.partition('от')
							cash_msk.append(int(head))
							continue
						else:
							cash_msk.append(int(prom))
							continue
			if i['city'] == "Санкт-Петербург":
				if i['cash'].find("руб")!= -1:
					int_rub_text=i['cash'].replace('\xa0','')
					head, sep, tail = int_rub_text.partition('руб')
					if head.find("от")!= -1:
						prom = head.replace('от','')
						if prom.find("до")!= -1:
							head, sep, tail = prom.partition('до')
							cash_spb.append(int(head))
							continue
						else:
							cash_spb.append(int(prom))
							continue
					if head.find("до")!= -1:
						prom = head.replace('до','')
						if prom.find("от")!= -1:
							head, sep, tail = prom.partition('от')
							cash_spb.append(int(head))
							continue
						else:
							cash_spb.append(int(prom))
							continue
			if i['city'] == "Казань":
				if i['cash'].find("руб")!= -1:
					int_rub_text=i['cash'].replace('\xa0','')
					head, sep, tail = int_rub_text.partition('руб')
					if head.find("от")!= -1:
						prom = head.replace('от','')
						if prom.find("до")!= -1:
							head, sep, tail = prom.partition('до')
							cash_kazan.append(int(head))
							continue
						else:
							cash_kazan.append(int(prom))
							continue
					if head.find("до")!= -1:
						prom = head.replace('до','')
						if prom.find("от")!= -1:
							head, sep, tail = prom.partition('от')
							cash_kazan.append(int(head))
							continue
						else:
							cash_kazan.append(int(prom))
							continue
			if i['city'] == "Екатеринбург":
				if i['cash'].find("руб")!= -1:
					int_rub_text=i['cash'].replace('\xa0','')
					head, sep, tail = int_rub_text.partition('руб')
					if head.find("от")!= -1:
						prom = head.replace('от','')
						if prom.find("до")!= -1:
							head, sep, tail = prom.partition('до')
							cash_ekb.append(int(head))
							continue
						else:
							cash_ekb.append(int(prom))
							continue
					if head.find("до")!= -1:
						prom = head.replace('до','')
						if prom.find("от")!= -1:
							head, sep, tail = prom.partition('от')
							cash_ekb.append(int(head))
							continue
						else:
							cash_ekb.append(int(prom))
							continue
			if i['city'] != "Санкт-Петербург" and i['city'] != "Москва"and i['city'] != "Казань" and i['city'] != "Екатеринбург":
				if i['cash'].find("руб")!= -1:
					int_rub_text=i['cash'].replace('\xa0','')
					head, sep, tail = int_rub_text.partition('руб')
					if head.find("от")!= -1:
						prom = head.replace('от','')
						if prom.find("до")!= -1:
							head, sep, tail = prom.partition('до')
							cash_region.append(int(head))
							continue
						else:
							cash_region.append(int(prom))
							continue
					if head.find("до")!= -1:
						prom = head.replace('до','')
						if prom.find("от")!= -1:
							head, sep, tail = prom.partition('от')
							cash_region.append(int(head))
							continue
						else:
							cash_region.append(int(prom))
							continue
				if i['cash'].find("USD")!= -1:
					int_usd_text=i['cash'].replace('\xa0','')
					head, sep, tail = int_usd_text.partition('USD')
					if head.find("от")!= -1:
						prom = head.replace('от','')
						if prom.find("до")!= -1:
							head, sep, tail = prom.partition('до')
							head = int(head) * 75.05
							cash_region.append(int(head))
							continue
						else:
							prom = int(prom) * 75.05
							cash_region.append(int(prom))
							continue				
					if head.find("до")!= -1:
						prom = head.replace('до','')
						if prom.find("от")!= -1:
							head, sep, tail = prom.partition('от')
							head = int(head) * 75.05
							cash_region.append(int(head))
							continue
						else:
							prom = int(prom) * 75.05
							cash_region.append(int(prom))
							continue					
				if i['cash'].find("KZT")!= -1:
					int_kzt_text=i['cash'].replace('\xa0','')
					head, sep, tail = int_kzt_text.partition('KZT')
					if head.find("от")!= -1:
						prom = head.replace('от','')
						if prom.find("до")!= -1:
							head, sep, tail = prom.partition('до')
							head = int(head) * 0.17
							cash_region.append(int(head))
							continue
						else:
							prom = int(prom) * 0.17
							cash_region.append(int(prom))
							continue					
					if head.find("до")!= -1:
						prom = head.replace('до','')
						if prom.find("от")!= -1:
							head, sep, tail = prom.partition('от')
							head = int(head) * 0.17							
							cash_region.append(int(head))
							continue
						else:
							prom = int(prom) * 0.17				
							cash_region.append(int(prom))
							continue					
				if i['cash'].find("EUR")!= -1:
					int_kzt_text=i['cash'].replace('\xa0','')
					head, sep, tail = int_kzt_text.partition('EUR')
					if head.find("от")!= -1:
						prom = head.replace('от','')
						if prom.find("до")!= -1:
							head, sep, tail = prom.partition('до')
							head = int(head) * 80.37
							cash_region.append(int(head))
							continue
						else:
							prom = int(prom) * 80.37
							print(prom)
							cash_region.append(int(prom))
							continue
					if head.find("до")!= -1:
						prom = head.replace('до','')
						if prom.find("от")!= -1:
							head, sep, tail = prom.partition('от')
							head = int(head) * 80.37
							cash_region.append(int(head))
							continue
						else:
							prom = int(prom) * 80.37
							cash_region.append(int(prom))
							continue
		except:
			pass
			
	
	try:
		avg_msk = sum(cash_msk)/len(cash_msk)
	except ZeroDivisionError:
		avg_msk = 0
	try:
		avg_spb = sum(cash_spb)/len(cash_spb)
	except ZeroDivisionError:
		avg_spb = 0
	try:
		avg_kazan = sum(cash_kazan)/len(cash_kazan)
	except ZeroDivisionError:
		avg_kazan = 0
	try:
		avg_ekb = sum(cash_ekb)/len(cash_ekb)
	except ZeroDivisionError:
		avg_ekb = 0
	try:
		avg_region = sum(cash_region)/len(cash_region)
	except ZeroDivisionError:
		avg_region = 0
	

	data_exp2 = {
		"Москва" : int(avg_msk),
		"Санкт-Петербург" : int(avg_spb),
		"Казань" : int(avg_kazan),
		"Екатеринбург" : int(avg_ekb),
		"Регионы" : int(avg_region)
	}


	plt.figure(figsize=(6, 5))
	courses_region = list(data_exp2.keys())
	values_region = list(data_exp2.values())
	barlot2 = plt.bar(courses_region, values_region, color ='blue', width = 0.3)
	plt.bar_label(barlot2,labels=values_region,label_type='edge')
	plt.title("Средняя зарплата по главным регионам")	
	fig2 = plt.gcf()    
	draw_figure(main_window['-CANVAS2-'].TKCanvas, fig2)
	figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
	plt.close()


	dict_table = make_array_from_list_of_dicts(content)
	main_window['-TABLE-'].update(values=dict_table, visible=True)
	main_window['-TEXT_diap-'].update(f'{int(data_cash[0])} - {int(data_cash[-1])} руб.')
	main_window['-TEXT_median-'].update(f'{int(median)} руб.')
	main_window['-TEXT_avg-'].update(f'{int(avg_cash)} руб.')
	write_in_file(data,dict_1)


def get_token():
	with open('data.json', 'r',) as fp:
		new_data = json.load(fp)
	return new_data[0]

def second_parse(window,dict_data,combo_resume,combo_vac,Multiline_text):
	with open('content.json', 'r',errors='ignore',encoding = 'utf-8') as fp:
		new_data = json.load(fp)
	if combo_vac == 'Все вакансии':
		for i in new_data:
			head, sep, tail = i['link'].partition('?')
			head, sep, tail = head.partition('vacancy/')
			print(Multiline_text)
			params = {'resume_id': dict_data[combo_resume], 'vacancy_id': tail, 'message': Multiline_text}
			response = requests.post('https://api.hh.ru/negotiations', headers = {'Authorization':f'Bearer {dict_data["Token"]}','Content-Type': 'multipart/form-data'}, params=params)
			if response.status_code == 201:
				msg = f'Отклик на вакансию "{i["name"]}" - успешно отправлен.'
				print(msg)
				window['-TEXT_response-'].update(msg)
			if response.status_code == 400:
				msg = f'Отклик на вакансию "{i["name"]}" - не был отправлен.'
				print(msg)
				window['-TEXT_response-'].update(msg)
			if response.status_code == 403:
				msg = f'Отклик на вакансию "{i["name"]}" - не был отправлен по причине отстутствия доступа к ней, отклик был сделан ранее или видимость резюме не позволяет откликнуться на вакансию.'
				print(msg)
				window['-TEXT_response-'].update(msg)
			time.sleep(10)
	else:
		head, sep, tail = combo_vac.partition(')')
		head, sep, tail = head.partition('(')
		id = tail
		params = {'resume_id': dict_data[combo_resume], 'vacancy_id': id, 'message': Multiline_text}
		response = requests.post('https://api.hh.ru/negotiations', headers = {'Authorization':f'Bearer {dict_data["Token"]}','Content-Type': 'multipart/form-data'}, params=params)
		if response.status_code == 201:
			msg = f'Отклик на вакансию "{combo_vac}" - успешно отправлен.'
			print(msg)
			window['-TEXT_response-'].update(msg)
		if response.status_code == 400:
			msg = f'Отклик на вакансию "{combo_vac}" - не был отправлен.'
			print(msg)
			window['-TEXT_response-'].update(msg)
		if response.status_code == 403:
			msg = f'Отклик на вакансию "{combo_vac}" - не был отправлен по причине отстутствия доступа к ней, отклик был сделан ранее или видимость резюме не позволяет откликнуться на вакансию.'
			print(msg)
			window['-TEXT_response-'].update(msg)


def make_win2():
	data = []
	data_name = []
	data_dict = {}
	token = get_token()
	data_dict["Token"] = token
	response = requests.get('https://api.hh.ru/resumes/mine', headers={'Authorization':f'Bearer {token}'})
	resumes = response.json()
	data_name.append('Все вакансии')
	for resume in resumes['items']:
		data.append(resume['title'])
		data_dict[resume['title']] = resume['id']
		data_dict['name'] = resume['id']
	with open('content.json', 'r',errors='ignore',encoding = 'utf-8') as fp:
		new_data = json.load(fp)
	for i in new_data:
		head, sep, tail = i['link'].partition('?')
		head, sep, tail = head.partition('vacancy/')
		data_name.append(i['name'] + '(' + tail + ')')
	layout = [
	[sg.Text('Выберите резюме:'), sg.Combo(values=data, readonly=True, key='combo_resume',expand_x = True)],
	[sg.Text('Выберите вакансию:'), sg.Combo(values=data_name, readonly=True, key='combo_vac',expand_x = True)],
	[sg.Multiline(s=(500,10),key = 'Multiline_text')],
	[sg.Button('Подтвердить',button_color=('black','white'), key='-Accept-')],
	[sg.Output(key='-TEXT_response-', expand_x=True, expand_y = True)]
	]
	window = sg.Window('Отклик на вакансии', layout, finalize=True,size=(700, 500))
	while True:
		event, values = window.read()
		if event == sg.WIN_CLOSED : # if user closes window or clicks cancel
			break
		elif event == '-Accept-':
			th1 = Thread(target=second_parse, args=(window,data_dict,values['combo_resume'],values['combo_vac'],values['Multiline_text'],))
			th1.start()			
	return window


def open_vac(counter):
	try:
		file1 = open('content.json', 'r',errors='ignore',encoding = 'utf-8')
	except FileNotFoundError:
		print('Контента нет')
	with file1 as fp:
		new_data = json.load(fp)
	link = new_data[int(counter)]['link']
	if link:
		chrome_options = Options()
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_experimental_option("detach", True)
		browser = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
		browser.get(link)
	else:
		print("Нет ссылки")
	

def make_window(theme=None):
	sg.theme(theme)
	right_click_menu = ['', ['Открыть вакансию в браузере']]
	headings = ["Должность", "Компания", "Зарплата", "Опыт работы", "Описание", "Город","Адрес", "Тип занятости", "Ключевые навыки", "Ссылка"]
	data_table = []
	#menu_def=['&File', ['&New File', '&Open...','Open &Module','---', '!&Recent Files','C&lose']],['&Save',['&Save File', 'Save &As','Save &Copy'  ]],['&Edit', ['&Cut', '&Copy', '&Paste']]
	layout_tab1 = [[sg.Table(values=data_table, headings=headings,  visible = True,  vertical_scroll_only = False, max_col_width=50,
                    auto_size_columns=True,
		    		right_click_selects=True,
                    num_rows=20,
		    		expand_x = True,
					justification='center', key='-TABLE-',
					selected_row_colors='red on yellow', 
					enable_click_events=True, 
					enable_events=True)]]
	layout_tab_exp = [
			[sg.Text('Опыт работы',font='Helvetica 18 bold')],
			[sg.Canvas(key='-CANVAS_circle-')],
	]

	layout_tab_cash = [[sg.Text('Анализ заработной платы										',font='Helvetica 18 bold')],
		    [sg.Text('Диапозон: '),sg.Text('',key='-TEXT_diap-')],
		    [sg.Text('Медиана зарплаты: '),sg.Text('',key='-TEXT_median-')],
		    [sg.Text('Средняя зарплата: '),sg.Text('',key='-TEXT_avg-')],
		    [sg.Canvas(key='-CANVAS-'),sg.Canvas(key='-CANVAS2-')]
		    ]
	tab_group = sg.TabGroup([[sg.Tab('Опыт работы', layout_tab_exp)],[sg.Tab('Анализ заработной платы', layout_tab_cash)]],border_width = 3)
	tab6_layout = [[tab_group]]
	layout = [ 
			#[sg.Menu(menu_def, key='-MENU-')],
			[sg.Button('Старт', button_color=('black','white'), key='Play'),sg.Button('Выход', button_color=('black','white'), key='-Stop-'), sg.Button('Откликнуться на вакансию(и)', button_color=('black','white'), key='otklic'), sg.Text('                                                                                                                                                                                   Тема:',justification='center'),sg.Combo(sg.theme_list(), default_value=sg.theme(), s=(15,22), enable_events=True, readonly=True, k='-Theme-')],
			[sg.HSep()],
			[sg.VSep(),sg.Text('Введите вакансию:'), sg.InputText(key='-VAC-',size=(40, 1)),sg.Text('Образование:'),sg.Combo(values=('Не требуется или не указано','Высшее', 'Среднее профессиональное'),  readonly=True, key='-COMBO-',expand_x=True),sg.VSep()],
			[sg.VSep(),sg.Text('Количество страниц (1 страница = 20 вакансий):'), sg.InputText(key='-PAGE-',size=(15, 1)),sg.Text('Опыт работы:'),sg.Combo(values=('Не имеет значения','От 1 до года до 3 лет', 'От 3 до 6 лет', 'Нет опыта', 'Больше 6 лет'), readonly=True, key='-COMBO_Exp-',expand_x=True),sg.VSep()],
			[sg.VSep(),sg.Text('Укажите регион(ы) через пробел:'), sg.InputText(key='-Region-',size=(28, 1)),sg.Text('График работы:'),sg.Combo(values=('Полный день','Сменный трафик', 'Гифкий график', 'Удаленная работа', 'Вахтовый метод'), readonly=True, key='-COMBO_time_work-',expand_x=True),sg.VSep()],
			[sg.VSep(),sg.Text('Укажите уровень дохода от:'), sg.InputText(key='-Salary-',size=(32, 1)),sg.Text('Тип занятости:'),sg.Combo(values=('Полная занятость','Частичная занятость', 'Проектная работа', 'Стажировка', 'Волонтерство'), readonly=True, key='-COMBO_employment-',expand_x=True),sg.VSep()],
			[sg.VSep(),sg.Text('Указан доход:'),sg.Checkbox('', default=False, key='-Checkbox-',expand_x=True),sg.VSep()],
			[sg.VSep(),sg.Text('Валюта:'),sg.Combo(values=('RUB','EUR', 'USD'), readonly=True, key='-COMBO_valuta-',expand_x=True),sg.VSep()],
			[sg.HSep()],
			[sg.TabGroup([[sg.Tab('Таблица', layout_tab1), sg.Tab('Статистика', tab6_layout)]])]]

	window = sg.Window('Вакансии HH.RU', layout, finalize=True, right_click_menu=right_click_menu, size=(1200, 850))
	
	return window


def parse():
	data_table = []
	window = make_window()	
	window2 = None
	while True:
		event, values = window.read()
		if isinstance(event, tuple): 
			answer = event[2][0]
		if event == sg.WIN_CLOSED or event == '-Stop-': # if user closes window or clicks cancel
			break
		if values['-Theme-'] != sg.theme():
			sg.theme(values['-Theme-'])
			window.close()
			window = make_window()
		if event == 'Открыть вакансию в браузере':
			th2 = Thread(target=open_vac, args=(answer,))
			th2.start()
		elif event == "Play":
			th = Thread(target=main_parse, args=(values['-VAC-'], values['-PAGE-'], values['-Salary-'], values['-Checkbox-'], 
					values['-Region-'], values['-COMBO-'],values['-COMBO_Exp-'], values['-COMBO_employment-'], values['-COMBO_time_work-'],
					values['-COMBO_valuta-'], data_table,window))
			th.start()	
		elif event == "otklic":
			window2 = make_win2()				
	window.close()

parse()	