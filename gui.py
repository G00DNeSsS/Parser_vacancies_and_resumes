from tkinter import *
from tkinter import ttk
from threading import Thread
import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

def selenium():
	chrome_options = Options()
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_experimental_option("detach", True)
	browser = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
	browser.get("https://hh.ru/login")
	time.sleep(30)
	link = browser.current_url
	if link == 'https://spb.hh.ru/?hhtmFrom=account_login':
		print(link)
		browser.get("https://hh.ru/oauth/authorize?response_type=code&client_id=M3RJAUA7MKSI9OFB32695SIBMR92DQMAQ54S9N97NPFC84F7QTE4G4V5PVKNG0BR")
	if link == 'https://spb.hh.ru/':
		print(link)
		browser.get("https://hh.ru/oauth/authorize?response_type=code&client_id=M3RJAUA7MKSI9OFB32695SIBMR92DQMAQ54S9N97NPFC84F7QTE4G4V5PVKNG0BR")


	

def init():
	
	sg.theme('Dark Amber') 
	data = []
	layout = [[sg.Text('Parser HH.RU',font='Helvetica 26 bold')],
	[sg.Button('Вакансии', button_color=('black','white'), size=(30,2),border_width=4,key='Vac', font='Helvetica 10 bold'),sg.Button('Резюме', button_color=('black','white'),border_width=4, size=(30,2), key='Resume', font='Helvetica 10 bold')],
	[sg.Button('Войти в личный кабинет', button_color=('black','white'), size=(30,2),border_width=4,key='LK', font='Helvetica 10 bold')],
	[sg.InputText(key='token',size=(50, 2))]
	]
	
	window = sg.Window('Parser HH.RU', layout,size=(1000, 600),element_justification='c',margins=(0,200))
	while True:
		event, values = window.read()
		if event == sg.WIN_CLOSED or event == '-Stop-': # if user closes window or clicks cancel
			break
		elif event == "Vac":
			window.close()
			data.append(values['token'])
			with open('data.json', 'w', encoding='utf-8') as f:
				json.dump(data, f, ensure_ascii=False, indent=4)
			import parse_vac
		elif event == "Resume":
			window.close()
			import parse_resume
		elif event == "LK":
			th = Thread(target=selenium)
			th.start()		
	window.close()
init()