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

  

play = b'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'
stop = b'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAABmJLR0QA/wD/AP+gvaeTAAAAaklEQVRoge3ZQQqAMAxFwSre/8p6AZFUiXzKzLqLPNJVOwYAvLcVzpztU9Q8zrr/NUW3Y+JsZXsdSjdimY0ISSMkjZA0QtIISSMkjZA0QtIISSMkjZA0QtIISSMkzcxrfMo/ya1lNgIAX1zq+ANHUjXZuAAAAABJRU5ErkJggg=='
eject = b'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAABmJLR0QA/wD/AP+gvaeTAAAByklEQVRoge3YO2gUURSA4S+JRnyACIGADyxERAsb0UKrWIidWIidlSA2YpFWSauNVtrYiIU2YpFCLGwEEWwsBAsLEbFQFARFfKBZizkyK5pkZvZmZ7PeH05z595z/sPszpxdMplMJpMZbDZFLGsm8CxiomWXxqzBQ3QiHmNdq0YNGMc9RQOvIjqxNt6iVy1GcF0h/h47sR1vY+0mRluzq8ElhfBn7O9a34tPce1KC161OK8Q/Y7D/7h+EF9jz7k+etXilELwJ44vsO8ofsTeM33wqsURpdzZCvtPK5s+toRetZjCF4XYTI1zM3HmGw4lt6rJbnxQCF1tcP5ynP2IPQm9arENb0LkDsYa5BjFrcjxDjuS2VVkI16EwH2s6iHXStxVvjy39GxXkfV4Iu3Y0T3OPMWGBDkXZDUeRMHnmEyY+/eA2cEjrE2Y+w/GcDsKvcbWJaixGS+jxixWpC4wgmvK+WlX6gJddM9lN6J2Mi4q56cDKRPPwz7lXHYhVdJp5W+KtmK61yZOYG4AGpnDyV6byWT+ZxZ7Rnf6YlGdeX2XxZ8AVag6AiR9uzZg0U/G0NyR3MigUfU7MmhPr78YmjuSyWQymUxmmPgFokSdfYSQKDwAAAAASUVORK5CYII='

bg = sg.LOOK_AND_FEEL_TABLE[sg.CURRENT_LOOK_AND_FEEL]['BACKGROUND']  


GRAPH_SIZE= (100,100) 

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


bc1 = b''

area = config.HEADHUNTER_AREA_PARAM

	
def init(name_resume, page_resume, region, salary_before, salary_after, salary_checkbox,relocation,
	exp,gender,gender_checbox,age_before, age_after,age_checkbox,education,employment,time_work,status_work,val):
	
	region_text = translite_region(region)
	text_work = name_resume
	text_work_rus=text_work
	text_work=transliterate(text_work)
	profession = text_work
	pages = page_resume
	d = {
		"prof": profession,
		"pages" : pages,
		"text_work_rus": text_work_rus,
		"salary_before":salary_before,
		"salary_after" : salary_after,
		"salary_checkbox" : salary_checkbox,
		"area" : region_text,
		"relocation" : relocation,
		"exp" : exp,
		"gender" : gender,
		"gender_checbox" : gender_checbox,
		"age_before": age_before,
		"age_after":age_after,
		"age_checkbox":age_checkbox,
		"education" : education,
		"employment" : employment,
		"work_time" : time_work,
		"status_work": status_work,
		"val" : val
	}
	return d

		

def get_response_resume(dict):
	content_links=[]
	URL = "https://hh.ru/search/resume?"
	if dict["prof"]:
		URL = URL + "text=" +dict["prof"] 
	
	if dict["salary_before"]:
		URL = URL + "&salary_from="+ dict["salary_before"]
	if dict["salary_after"]:
		URL = URL + "&salary_to="+ dict["salary_after"]
	
	if dict["salary_checkbox"] == True:
		URL = URL + "&label=only_with_salary"
	if dict["salary_checkbox"] == False:
		URL = URL
	
	for item in dict['area']:
		if item == "2":
			URL = URL + "&area=2"	
		if item == "1":
			URL = URL + "&area=1"
	
	if dict["relocation"]:
		if dict["relocation"] == "Живут или готовы переехать в регион":
			URL = URL + "&relocation=living_or_relocation"
		if dict["relocation"] == "Живут в регионе":
			URL = URL + "&relocation=living"
		if dict["relocation"] == "Готовы уехать из региона":
			URL = URL + "&relocation=living_but_relocation"
		if dict["relocation"] == "Не живут, но готовы переехать в регион":
			URL = URL + "&relocation=relocation"
	
	if dict["exp"]:
		if dict["exp"] == "От 1 до года до 3 лет":
			URL = URL + "&experience=between1And3"
		if dict["exp"] == "От 3 до 6 лет":
			URL = URL + "&experience=between3And6"
		if dict["exp"] == "Нет опыта":
			URL = URL + "&experience=noExperience"
		if dict["exp"] == "Больше 6 лет":
			URL = URL + "&experience=moreThan6"
	
	if dict["gender"]:
		if dict["gender"] == "Мужской":
			URL = URL + "&gender=male"
		if dict["gender"] == "Женский":
			URL = URL + "&gender=female"
		if dict["gender"] == "Не имеет значения":
			URL = URL + "&gender=unknown"
	
	if dict["gender_checbox"] == True:
		URL = URL + "&label=only_with_gender"
	if dict["gender_checbox"] == False:
		URL = URL

	if dict["age_before"]:
		URL = URL + "&age_from="+ dict["age_before"]
	if dict["age_after"]:
		URL = URL + "&age_to="+ dict["age_after"]

	if dict["age_checkbox"] == True:
		URL = URL + "&label=only_with_age"
	if dict["age_checkbox"] == False:
		URL = URL

	if dict["education"]:
		if dict["education"] == "Среднее":
			URL = URL + "&education_level=secondary"	
		if dict["education"] == "Среднее специальное":
			URL = URL + "&education_level=special_secondary"
		if dict["education"] == "Незаконченное высшее":
			URL = URL + "&education_level=unfinished_higher"
		if dict["education"] == "Бакалавр":
			URL = URL + "&education_level=bachelor"
		if dict["education"] == "Магистр":
			URL = URL + "&education_level=master"
		if dict["education"] == "Высшее":
			URL = URL + "&education_level=higher"
		if dict["education"] == "Кандидат наук":
			URL = URL + "&education_level=candidate"
		if dict["education"] == "Доктор наук":
			URL = URL + "&education_level=doctor"
	
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

	if dict["status_work"]:
		if dict["status_work"] == "Без статуса поиска":
			URL = URL + "&job_search_status=unknown"
		if dict["status_work"] == "Не ищет работу":
			URL = URL + "&job_search_status=not_looking_for_job"
		if dict["status_work"] == "Рассматривает предложения":
			URL = URL + "&job_search_status=looking_for_offers"
		if dict["status_work"] == "Активно ищет работу":
			URL = URL + "&job_search_status=active_search"
		if dict["status_work"] == "Предложили работу, решает":
			URL = URL + "&job_search_status=has_job_offer"
		if dict["status_work"] == "Вышел на новое место":
			URL = URL + "&job_search_status=accepted_job_offer"

	if dict["val"]:
		if dict["val"] == "RUB":
			URL = URL + "&currency_code=rub"
		if dict["val"] == "EUR":
			URL = URL + "&currency_code=EUR"
		if dict["val"] == "USD":
			URL = URL + "&currency_code=USD"
		

	for pag in range(int(dict['pages'])):
		URL_main =  URL +"&ored_clusters=true&order_by=relevance&logic=normal&pos=full_text&exp_period=all_time" +"&page="+str(pag) 
		print(URL_main)
		content_links.append({
			"link": URL_main
		})	
	return content_links



def get_page_content_resume(content_links,dict):
	'''Поиск всех данных на одной конкретной page'''
	content = []
	content1 = []
	text = '•'
	last_text = ''
	education_last = ''
	language_last=''
	expirience_last = ''
	space = " "
	new_str = '\n'
	data_education = []
	for response_links in content_links:
		response = requests.get(
			response_links["link"], headers=config.HEADERS)
		soup = BeautifulSoup(response.text, "html.parser")
		vacancies = soup.find_all("div", class_="serp-item")
		if len(vacancies) == 0:
			continue
		else:
			for vac in vacancies:
				vac_str = vac.find('a', attrs={'class' : 'serp-item__title', 'data-qa': 'serp-item__title', 'target':'_blank'}).get("href")
				vacancies_last = "https://hh.ru" + vac_str
				content.append(
					{	
						"link" : vacancies_last
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
				age = result.find('span', attrs={'data-qa': 'resume-personal-age'})
				gender = result.find('span', attrs={'data-qa': 'resume-personal-gender'})
				birthday = result.find('span', attrs={'data-qa': 'resume-personal-birthday'})
				city = result.find('span', attrs={'data-qa': 'resume-personal-address'})
				job = result.find('span', attrs={'class' : 'resume-block__title-text', 'data-qa' : 'resume-block-title-position'})
				cash = result.find('span', attrs={'class' : 'resume-block__salary', 'data-qa' : 'resume-block-salary'})
				resume_position = result.find("div", {"class": "resume-block", "data-qa": "resume-block-position"})
				if resume_position is not None:
					specialization = resume_position.find_all('li')
					if specialization is not None:
						for r in specialization:
							if r:
								interim = " ".join(str(new) for new in r)
								specialization_new_text = interim.replace('<li class="resume-block__specialization" data-qa="resume-block-position-specialization">', '').replace('</li>', '')
								last_text = last_text+text+specialization_new_text+space
				else:
					last_text = 'Нет спициализации'
				
				
				if age:
					age_text = age.get_text(strip=True)
					nums = re.findall(r'\d+', age_text)
					nums = [int(i) for i in nums]
					age_text = nums
					age_count = " ".join(str(з) for з in age_text)
					age_text = age_count.replace('[','').replace(']',' ')		
				else:
					age_text = "Нет возраста"


				if gender:
					gender_text = gender.get_text(strip=True)
				else:
					gender_text = "Не указан пол"
					
				if birthday:
					birthday_text = birthday.get_text(strip=True)
				else:
					birthday_text = "Не указана дата рождения"
					
				if city:
					city_text = city.get_text(strip=True)
				else:
					city_text = "Не указан город"	
				
				if job:
					job_text = job.get_text(strip=True)
				else:
					job_text = "Не указана должность"

				if cash:
					cash_text = cash.get_text(strip=True).replace('\u2009', '').replace('\xa0', ' ')
				else:
					cash_text = "Не указано"	
				
				busyness = result.find(lambda tag: tag.name == 'p' and 'График работы:' in tag.text)
				if busyness:
					interim_new = " ".join(str(c) for c in busyness)
					busyness_text = interim_new.replace('<p>График работы: <!-- -->','').replace('</p>','').replace('График работы:    ','')
				else: 
					busyness_text = "Не указано"

				work_time = result.find(lambda tag1: tag1.name == 'p' and 'Занятость:' in tag1.text)
				if work_time:
					interim_new_last = " ".join(str(c1) for c1 in work_time)
					work_time_text = interim_new_last.replace('<p>Занятость: <!-- -->','').replace('</p>','').replace('Занятость:    ','')
				else:
					work_time_text = "Не указано"
				

				education = result.find("div", {"class": "resume-block", "data-qa": "resume-block-education"})
				if education is not None:
					education = education.find("div", {"class": "resume-block-item-gap"}).find("div", {"class": "bloko-columns-row"})
					for education_item in education.findAll("div", {"class": "resume-block-item-gap"}):
						year = education_item.find("div", {"class": "bloko-column bloko-column_xs-4 bloko-column_s-2 bloko-column_m-2 bloko-column_l-2"})
						if year is not None:
							year = year.get_text()
						else:
							year = "Не указан"
						item_name = education_item.find("div", {"data-qa": "resume-block-education-name"})
						if item_name is not None:
							item_name = item_name.get_text()
						else:
							item_name = "Не указан"
						item_organization = education_item.find("div", {"data-qa": "resume-block-education-organization"})
						if item_organization is not None:
							item_organization = item_organization.get_text()
						else:
							item_organization = "Не указан"
						education_last = education_last +  text + "Год окончания: " + year + space + "Учебное заведение: " + item_name + space + "Специальность: " + item_organization
				
				education1 = result.find("div", {"class": "resume-block", "data-qa": "resume-block-education"})
				if education1 is not None:
					education_level = education1.find("span", {"class": "resume-block__title-text resume-block__title-text_sub"}).get_text()
				else: 
					education_level = 'Нет образования'
				
				language = result.find_all('p', attrs={'data-qa' : 'resume-block-language-item'})
				for item_language in language:
					language_prom = " ".join(str(new_string) for new_string in item_language)
					item_language_new = language_prom.replace('<p data-qa="resume-block-language-item">', '').replace('    ', ' ').replace('</p>', '')
					language_last = language_last+text+item_language_new+space

				expirience = result.find("div", {"class": "resume-block", "data-qa": "resume-block-experience"})
				if expirience is not None:
					expirience = expirience.find("div", {"class": "resume-block-item-gap"}).find("div", {"class": "bloko-columns-row"})
					for expirience_item in expirience.find_all('div', {'class': 'resume-block-item-gap'}):

						time = expirience_item.find("div", {"class": "bloko-column bloko-column_xs-4 bloko-column_s-2 bloko-column_m-2 bloko-column_l-2"})
						if time:
							time_text = time.get_text(strip=True)
						else:
							time_text = 'Нет интервала времени'
							
						place_job = expirience_item.find("div", {'class' : 'bloko-text bloko-text_strong'})
						if place_job:
							place_job_text = place_job.get_text(strip=True)	
						else:
							place_job_text = 'Нет место работы'
							
						name_job = expirience_item.find("div", {'class' : 'bloko-text bloko-text_strong', 'data-qa' : 'resume-block-experience-position'})
						if name_job:
							name_job_text = name_job.get_text(strip=True)
						else:
							name_job_text = 'Не указана должность'
							
						description = expirience_item.find("div", {'data-qa' : 'resume-block-experience-description'})
						if description:
							description_text = description.get_text(strip=True)
						else:
							description_text = 'Не указано описание'
						expirience_last = expirience_last + text + "Интервал работы: " + time_text + " Место работы: " + place_job_text + " Должность: " + name_job_text + " Описание: " + description_text

				expirience_count = result.find(lambda tag3: tag3.name == 'span' and 'Опыт работы' in tag3.text)
				if expirience_count:
					expirience_count_new = " ".join(str(з) for з in expirience_count)
					expirience_count_text = expirience_count_new.replace('Опыт работы  <span>','').replace('</span>   <span>',' ').replace('</span>','').replace('<!-- -->','')		
				else:
					expirience_count_text = "Не указано"
				
				content1.append(
					{	
						"gender" : gender_text,
						"age" : age_text,
						"birthday" : birthday_text, 
						"city" : city_text,
						"job" : job_text,
						"cash" : cash_text,#Крах
						"specialization" : last_text,
						"work_time" : busyness_text, #График работы
						"employment" : work_time_text,#Занятость
						"education" : education_last,
						"education_level" : education_level,
						"language" : language_last,
						"expirience": expirience_last,
						"expirience_count": expirience_count_text,
						"link" : i['link']
					}
				)
				
				last_text = ''
				education_last = ''
				language_last = ''
				expirience_last = ''
	return content1
	

def write_in_file_resume(data,dict):
	try:
		with open(f"{dict['text_work_rus'].title()}.{config.SAVE_FILE_EXTENSION}", "w", newline="",errors='ignore') as file:
			writer = csv.writer(file, delimiter=";")

			writer.writerow(["Пол","Возраст","Дата рождения", "Город проживания", "Желаемая должность" ,"Специализация", "График работы", "Занятость", "Уровень образования", "Подробности образования", "Языки", "Опыт работы", "Подробности прошлых мест", "Ссылки на резюме", "Желаемая зарплата"])

			for dataset in data:
				writer.writerow([dataset["gender"],dataset["age"],dataset["birthday"],dataset["city"], dataset["job"],dataset["specialization"], dataset["work_time"], dataset["employment"], dataset["education_level"], dataset["education"], dataset["language"], dataset["expirience_count"], dataset["expirience"], dataset["link"],dataset["cash"]])

		print(f"{'Файл Резюме -'+dict['text_work_rus'].title()}.{config.SAVE_FILE_EXTENSION} сохранён на рабочий стол!")
	except:
		print("Ошибка при записи в файл.")
	

def make_array_from_list_of_dicts(list_of_dicts):
    return [[i for i in j.values()] for j in list_of_dicts]


	
	
def main_parse(resume, page, region, salary_before, salary_after, salary_checkbox,relocation, exp,gender,gender_checbox, age_before, age_after,age_checkbox,education,employment,time_work,status_work, val,dict_table,main_window):
	dict_1 = init(resume,page,region,salary_before, salary_after, salary_checkbox,relocation,exp,gender,gender_checbox,age_before, age_after,age_checkbox,education,employment,time_work,status_work,val)
	responses = []
	responses.append(get_response_resume(dict_1))
	data = []
	age_20 = 0
	age_20_30 = 0
	age_30_40 = 0
	age_40_50 = 0
	age_50_60 = 0
	age_more_60 = 0
	age_no_age = 0

	exp_no_age = 0
	exp_1_3=0
	exp_3_6=0
	exp_more_6=0
	if get_page_content_resume(responses[0],dict_1) == None:
		print("По вашему запросу ничего не найдено!")
	else:
		for resp in responses:
			content = get_page_content_resume(resp,dict_1)
			if content != None:
				for dataset in content:
					data.append(dataset)	
			else:
				break
	
	dict_table = make_array_from_list_of_dicts(content)
	main_window['-TABLE-'].update(values=dict_table, visible=True)
	write_in_file_resume(data,dict_1)
	#подсчитать проценты тех у кого возраст больше 20 и меньше 30 в dict_1['age']
	for i in data:
		try:
			if int(i['age']) < 20 :
				age_20 = age_20 +1
			if int(i['age']) >= 20 and int(i['age']) < 30:
				age_20_30 = age_20_30 +1
			if int(i['age']) >= 30 and int(i['age']) < 40:
				age_30_40 = age_30_40 +1
			if int(i['age']) >= 40 and int(i['age']) < 50:
				age_40_50 = age_40_50 +1
			if int(i['age']) >= 50 and int(i['age']) < 60:
				age_50_60 = age_50_60 +1
			if int(i['age']) >= 60:
				age_more_60 = age_more_60 +1
		except:
			age_no_age = age_no_age +1
			pass

	percent_20 = age_20/len(data) * 100	
	percent_20_30 = age_20_30 / len(data) * 100
	percent_30_40 =age_30_40 / len(data) * 100
	percent_40_50 = age_40_50 / len(data) * 100
	percent_50_60 = age_50_60 / len(data) * 100
	percent_60 = age_more_60 / len(data) * 100
	percent_no_age = age_no_age / len(data) * 100


	for i in data:
		nums = re.findall(r'\d+', i['expirience_count'])
		nums = [int(b) for b in nums]
		exp_text = nums
		exp_count = " ".join(str(з) for з in exp_text)
		exp_text = exp_count.replace('[','').replace(']',' ')
		head, sep, tail = exp_text.partition(' ')
		try:
			if int(head) >= 1 and  int(head) < 3:
				exp_1_3 = exp_1_3+1
			if int(head) >= 3 and  int(head) < 6:
				exp_3_6 = exp_3_6+1
			if int(head) >= 6:
				exp_more_6 = exp_more_6+1
		except:
			exp_no_age = exp_no_age+1
			pass

	percent_exp_1_3 = exp_1_3/len(data) * 100	
	percent_exp_3_6 = exp_3_6/len(data) * 100	
	percent_exp_6 = exp_more_6/len(data) * 100	
	percent_no_exp = exp_no_age / len(data) * 100



	main_window['-TABLE-'].update(values=dict_table, visible=True)

	main_window['-TEXT_20-'].set_size((int(percent_20),1))
	main_window['-TEXT_20_proc-'].update(f'{int(percent_20)}%')

	main_window['-TEXT_20_30-'].set_size((int(percent_20_30),1))
	main_window['-TEXT_20_30_proc-'].update(f'{int(percent_20_30)}%')

	main_window['-TEXT_30_40-'].set_size((int(percent_30_40),1))
	main_window['-TEXT_30_40_proc-'].update(f'{int(percent_30_40)}%')

	main_window['-TEXT_40_50-'].set_size((int(percent_40_50),1))
	main_window['-TEXT_40_50_proc-'].update(f'{int(percent_40_50)}%')

	main_window['-TEXT_50_60-'].set_size((int(percent_50_60),1))
	main_window['-TEXT_50_60_proc-'].update(f'{int(percent_50_60)}%')

	main_window['-TEXT_60-'].set_size((int(percent_60),1))
	main_window['-TEXT_60_proc-'].update(f'{int(percent_60)}%')

	main_window['-TEXT_no_age-'].set_size((int(percent_no_age),1))
	main_window['-TEXT_no_age_proc-'].update(f'{int(percent_no_age)}%')

	


	main_window['-TEXT_exp_no-'].set_size((int(percent_no_exp),1))
	main_window['-TEXT_exp_no_proc-'].update(f'{int(percent_no_exp)}%')

	main_window['-TEXT_1_3_exp-'].set_size((int(percent_exp_1_3),1))
	main_window['-TEXT_1_3_exp_proc-'].update(f'{int(percent_exp_1_3)}%')

	main_window['-TEXT_3_6_exp-'].set_size((int(percent_exp_3_6),1))
	main_window['-TEXT_3_6_exp_proc-'].update(f'{int(percent_exp_3_6)}%')

	main_window['-TEXT_mpre_6_exp-'].set_size((int(percent_exp_6),1))
	main_window['-TEXT_more_6_proc-'].update(f'{int(percent_exp_6)}%')


def make_window(theme=None):
	sg.theme(theme)
	headings = ["Пол","Возраст","Дата рождения", "Город проживания", "Желаемая работа", "Желаемая зарплата", 
	"Специализация", "График работы", "Занятость", "Подробности образования", "Уровени образования", 
	"Языки", "Подробности опыта работы", "Опыт работы", "Ссылка"]
	data_table = []
	layout_tab1 = [[sg.Table(values=data_table, headings=headings,  visible = True,  vertical_scroll_only = False, max_col_width=40,
                    auto_size_columns=True,
		    		right_click_selects=True,
                    num_rows=50,
					justification='center', key='-TABLE-',
					selected_row_colors='red on yellow', 
					enable_events=True)]]
	
	layout_tab_age = [
			[sg.Text('Возраст',font='Helvetica 18 bold')],
			[sg.Text('До 20 лет'),sg.VSep(),sg.Text('', size=(0, 1),  background_color='yellow',key='-TEXT_20-'),sg.Text('',key='-TEXT_20_proc-')],
			[sg.Text('20 - 30 лет'),sg.VSep(),sg.Text('', size=(0, 1),  background_color='yellow',key='-TEXT_20_30-'),sg.Text('',key='-TEXT_20_30_proc-')],
			[sg.Text('30 - 40 лет'),sg.VSep(),sg.Text('', size=(0, 1),  background_color='yellow',key='-TEXT_30_40-'),sg.Text('',key='-TEXT_30_40_proc-')],
			[sg.Text('40 - 50 лет'),sg.VSep(),sg.Text('', size=(0, 1),  background_color='yellow',key='-TEXT_40_50-'),sg.Text('',key='-TEXT_40_50_proc-')],
			[sg.Text('50 - 60 лет'),sg.VSep(),sg.Text('', size=(0, 1),  background_color='yellow',key='-TEXT_50_60-'),sg.Text('',key='-TEXT_50_60_proc-')],
			[sg.Text('От 60 лет'),sg.VSep(),sg.Text('', size=(0, 1),  background_color='yellow',key='-TEXT_60-'),sg.Text('',key='-TEXT_60_proc-')],
			[sg.Text('Не указан '),sg.VSep(),sg.Text('', size=(0, 1),  background_color='yellow',key='-TEXT_no_age-'),sg.Text('',key='-TEXT_no_age_proc-')]]
	
	layout_tab_exp = [
			[sg.Text('Опыт работы',font='Helvetica 18 bold')],
			[sg.Text('Нет опыта'),sg.VSep(),sg.Text('', size=(0, 1),  background_color='yellow',key='-TEXT_exp_no-'),sg.Text('',key='-TEXT_exp_no_proc-')],
			[sg.Text('От 1 до 3 лет'),sg.VSep(),sg.Text('', size=(0, 1),  background_color='yellow',key='-TEXT_1_3_exp-'),sg.Text('',key='-TEXT_1_3_exp_proc-')],
			[sg.Text('От 3 до 6 лет '),sg.VSep(),sg.Text('', size=(0, 1),  background_color='yellow',key='-TEXT_3_6_exp-'),sg.Text('',key='-TEXT_3_6_exp_proc-')],
			[sg.Text('Более 6 лет'),sg.VSep(),sg.Text('', size=(0, 1),  background_color='yellow',key='-TEXT_mpre_6_exp-'),sg.Text('',key='-TEXT_more_6_proc-')],
	]
	tab_group = sg.TabGroup([[sg.Tab('Возраст', layout_tab_age)],[sg.Tab('Опыт работы', layout_tab_exp)]])
	

	tab6_layout = [[tab_group]]
	layout = [ 
			[sg.Button('Старт', button_color=('black','white'), key='Play'),sg.Button('Выход', button_color=('black','white'), key='-Stop-'),sg.Text('                                                                                                                                                                                   Тема:',justification='center'),sg.Combo(sg.theme_list(), default_value=sg.theme(), s=(15,22), enable_events=True, readonly=True, k='-Theme-')],
			[sg.HSep()],
			[sg.VSep(),sg.Text('Введите резюме:*'), sg.InputText(key='-VAC-',size=(50, 1)),sg.Text('Опыт работы:'),sg.Combo(values=('От 1 до года до 3 лет', 'От 3 до 6 лет', 'Нет опыта', 'Больше 6 лет'), readonly=True, key='-COMBO_Exp-',expand_x=True),sg.VSep()],
			[sg.VSep(),sg.Text('Количество страниц (1 страница = 20 резюме):*'), sg.InputText(key='-PAGE-',size=(24, 1)),sg.Text('Образование:'),sg.Combo(values=('Среднее','Среднее специальное', 'Незаконченное высшее','Бакалавр','Магистр','Высшее','Кандидат наук','Доктор наук '),  readonly=True, key='-COMBO_education-',expand_x=True),sg.VSep()],
			[sg.VSep(),sg.Text('Укажите регион(ы) через пробел:'), sg.InputText(key='-Region-',size=(36, 1)),sg.Text('Переезд:'),sg.Combo(values=('Живут или готовы переехать в регион','Живут в регионе', 'Готовы уехать из региона','Не живут, но готовы переехать в регион'),  readonly=True, key='-COMBO_relocation-',expand_x=True),sg.VSep()],
			[sg.VSep(),sg.Text('Уровень дохода: от'),sg.InputText(key='-Salary_before-',size=(25, 1)),sg.Text('до'),sg.InputText(key='-Salary_after-',size=(16, 1)),sg.Text('График работы:'),sg.Combo(values=('Полный день','Сменный трафик', 'Гифкий график', 'Удаленная работа', 'Вахтовый метод'), readonly=True, key='-COMBO_time_work-',expand_x=True),sg.VSep()],
			[sg.VSep(),sg.Text('Возраст в годах: от'),sg.InputText(key='-Age_before-',size=(25, 1)),sg.Text('до'),sg.InputText(key='-Age_after-',size=(16, 1)),sg.Text('Тип занятости:'),sg.Combo(values=('Полная занятость','Частичная занятость', 'Проектная работа', 'Стажировка', 'Волонтерство'), readonly=True, key='-COMBO_employment-',expand_x=True),sg.VSep()],
			[sg.VSep(),sg.Text('Указан доход:'),sg.Checkbox('', default=False, key='-Checkbox-'),sg.Text('Указан возраст:'),sg.Checkbox('', default=False, key='-Checkbox_age-'),sg.Text('Указан пол:'),sg.Checkbox('', default=False, key='-Checkbox_gender-'),
				sg.Text('Пол:'),sg.Combo(values=('Мужской', 'Женский', 'Не имеет значения'), readonly=True, key='-COMBO_gender-',expand_x=True),
    			sg.Text('Статус поиска:'),sg.Combo(values=('Без статуса поиска','Не ищет работу', 'Рассматривает предложения', 'Активно ищет работу', 'Предложили работу, решает','Вышел на новое место'), readonly=True, key='-COMBO_status_work-'),sg.VSep()],
			[sg.VSep(),sg.Text('Валюта:'),sg.Combo(values=('RUB','EUR', 'USD'), readonly=True, key='-COMBO_valuta-',expand_x=True),sg.VSep()],
			[sg.HSep()],
			[sg.TabGroup([[sg.Tab('Таблица', layout_tab1), sg.Tab('Статистика', tab6_layout)]])],
			]
	window = sg.Window('Резюме HH.RU', layout,size=(1000, 600))	
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
			th = Thread(target=main_parse, args=(values['-VAC-'], values['-PAGE-'],values['-Region-'],values['-Salary_before-'],values['-Salary_after-'],
					values['-Checkbox-'],values['-COMBO_relocation-'],values['-COMBO_Exp-'],values['-COMBO_gender-'],values['-Checkbox_gender-'],
					values['-Age_before-'],values['-Age_after-'],values['-Checkbox_age-'],values['-COMBO_education-'],values['-COMBO_employment-'],
					values['-COMBO_time_work-'],values['-COMBO_status_work-'], values['-COMBO_valuta-'], data_table,window))
			th.start()							
	window.close()
		

parse()	
