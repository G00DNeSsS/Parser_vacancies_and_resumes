from tkinter import *
from tkinter import ttk

import PySimpleGUI as sg


def init():
	sg.theme('Dark Amber') 
	layout = [[sg.Text('Parser HH.RU',font='Helvetica 26 bold')],
	[sg.Button('Вакансии', button_color=('black','white'), size=(30,2),border_width=4,key='Vac', font='Helvetica 10 bold'),sg.Button('Резюме', button_color=('black','white'),border_width=4, size=(30,2), key='Resume', font='Helvetica 10 bold')]
	]
	window = sg.Window('Parser HH.RU', layout,size=(1000, 600),element_justification='c',margins=(0,200))
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
	window.close()
init()