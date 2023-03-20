from tkinter import *
from tkinter import ttk
from threading import Thread
import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from seleniumwire import webdriver
import time
import json
import requests



def requests_token(token):
	data = []
	params = {'grant_type': 'authorization_code ', 'client_id': 'M3RJAUA7MKSI9OFB32695SIBMR92DQMAQ54S9N97NPFC84F7QTE4G4V5PVKNG0BR', 'client_secret': 'OS8JE8DTVS9IDF0O9CD87DSAN9LO9H488RVM3TV235M9MTRR588PLKA538JSQ15R', 'code' : token}
	response = requests.post('https://hh.ru/oauth/token', params = params) 
	dict_response = response.text
	parsed = json.loads(dict_response)
	data.append(parsed['access_token'])
	with open('data.json', 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False, indent=4)

def selenium(window):
	capabilities = DesiredCapabilities.CHROME
	capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+
	chrome_options = Options()
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('ignore-certificate-errors')
	chrome_options.add_experimental_option("detach", True)
	browser = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options, desired_capabilities=capabilities)
	browser.get("https://hh.ru/login")
	time.sleep(20)
	link = browser.current_url
	if link == 'https://spb.hh.ru/?hhtmFrom=account_login':
		print(link)
		browser.get("https://hh.ru/oauth/authorize?response_type=code&client_id=M3RJAUA7MKSI9OFB32695SIBMR92DQMAQ54S9N97NPFC84F7QTE4G4V5PVKNG0BR")
		time.sleep(10)
		for request in browser.requests:
			if request.response:
				if request.url == 'https://hh.ru/oauth/authorize?response_type=code&client_id=M3RJAUA7MKSI9OFB32695SIBMR92DQMAQ54S9N97NPFC84F7QTE4G4V5PVKNG0BR': 
					if request.response.headers['location'] is not None:
						head, sep, tail = request.response.headers['location'].partition('myapp://auth?code=')
						requests_token(tail)	
					else:
						continue
		browser.close()
		window['Vac'].update(visible=True)
		window['Resume'].update(visible=True)	
	if link == 'https://spb.hh.ru/':
		browser.get("https://hh.ru/oauth/authorize?response_type=code&client_id=M3RJAUA7MKSI9OFB32695SIBMR92DQMAQ54S9N97NPFC84F7QTE4G4V5PVKNG0BR")
		time.sleep(10)
		for request in browser.requests:
			if request.response:
				if request.url == 'https://hh.ru/oauth/authorize?response_type=code&client_id=M3RJAUA7MKSI9OFB32695SIBMR92DQMAQ54S9N97NPFC84F7QTE4G4V5PVKNG0BR': 
					if request.response.headers['location'] is not None:
						head, sep, tail = request.response.headers['location'].partition('myapp://auth?code=')
						requests_token(tail)	
					else:
						continue
		browser.close()				
		window['Vac'].update(visible=True)
		window['Resume'].update(visible=True)		

def init():
	sg.theme('Dark Amber') 
	layout = [[sg.Text('Parser HH.RU',font='Helvetica 26 bold')],
	[sg.Button('Войти в личный кабинет Head Hunter', button_color=('black','white'), size=(43,2),border_width=4,key='LK', font='Helvetica 10 bold')],
	[sg.Button('Вакансии', button_color=('black','white'), size=(30,2),border_width=4,key='Vac', font='Helvetica 10 bold',visible = False),sg.Button('Резюме', button_color=('black','white'),border_width=4, size=(30,2), key='Resume', font='Helvetica 10 bold',visible = False)]
	]
	
	window = sg.Window('Parser HH.RU', layout,size=(1000, 600),element_justification='c',margins=(0,180))
	while True:
		event, values = window.read()
		if event == sg.WIN_CLOSED or event == '-Stop-': # if user closes window or clicks cancel
			break
		elif event == "Vac":
			window.close()
			import parse_vac
		elif event == "Resume":
			window.close()
			import parse_resume
		elif event == "LK":
			th = Thread(target=selenium, args=(window,))
			th.start()					
	window.close()
init()