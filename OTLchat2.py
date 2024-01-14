## NOTES ##
'''
Mode:		Read/Write		Validated Parties:	
Name:		Status:			
Phrase:		Bogeys:						
Address:					Wait Time:

Status:
Not Setup
Not Secure
Pre-Contact
Secure
Secure - Bogeys

1. add check path for address
'''



## DEPENDENCIES ## 

import tkinter as tk
import tkinter.font as tkf
import pyfiglet
import time

## DEFINITIONS ##

class OTL:
	def __init__(self):

		self.info = {
			'Mode': ['Intranet Files', 'normal'],
			'Name': ['Not Set', 'blue'],
			'Phrase': ['Not Set', 'blue'],
			'Address': ['Not Set', 'blue'],
			'Read/Write': ['Idle', 'normal'],
			'Status': ['Not Setup', 'blue'],
			'Bogeys': ['0', 'green'],
			'Parties': ['usher', 'fox']
			}

		self.clock = {
			'status': 'stopped',
			'starttime': '',
			'delta': 0,
			'time': '00:00',
			}

		self.root = tk.Tk()
		self.root.title('OTL')
		self.root.configure(bg='black')

		self.root.columnconfigure(0, weight=0)
		self.root.columnconfigure(1, weight=0)
		self.root.columnconfigure(2, weight=0)
		self.root.columnconfigure(3, weight=1)
		self.root.rowconfigure(0, weight=0)
		self.root.rowconfigure(1, weight=0)
		self.root.rowconfigure(2, weight=1)
		self.root.rowconfigure(3, weight=0)

		self.headerwin = tk.Text(self.root)
		self.headerwin.insert('1.0', '\n' + pyfiglet.figlet_format('OTL',
			font = 'slant'))
		self.headerwin.config(
			bg='black',
			fg='orange',
			height=6,
			width=19,
			borderwidth=0,
			highlightthickness=0,
			state='disabled')
		self.headerwin.grid(row=0, column=0, rowspan=2, padx=5, sticky='nsew')

		self.infowin1 = tk.Text(self.root)
		self.infowin1.config(
			bg='black',
			fg='grey40',
			height=5,
			width=30,
			borderwidth=0,
			highlightthickness=0,
			font='Courier',
			wrap=tk.NONE,
			state='disabled')
		self.infowin1.tag_config('normal', foreground='grey40')
		self.infowin1.tag_config('blue', foreground='blue')
		self.infowin1.tag_config('green', foreground='green')
		self.infowin1.tag_config('orange', foreground='orange')
		self.infowin1.tag_config('red', foreground='red')
		self.infowin1.grid(row=0, column=1, sticky='nsew')

		self.infowin2 = tk.Text(self.root)
		self.infowin2.config(
			bg='black',
			fg='grey40',
			height=5,
			width=30, 
			borderwidth=0,
			highlightthickness=0,
			font='Courier',
			wrap=tk.NONE,
			state='disabled')
		self.infowin2.tag_config('normal', foreground='grey40')
		self.infowin2.tag_config('blue', foreground='blue')
		self.infowin2.tag_config('green', foreground='green')
		self.infowin2.tag_config('orange', foreground='orange')
		self.infowin2.tag_config('red', foreground='red')
		self.infowin2.grid(row=0, column=2, sticky='nsew')

		self.infowin3 = tk.Text(self.root)
		self.infowin3.config(
			bg='black',
			fg='grey40',
			height=5,
			width=30,
			borderwidth=0,
			highlightthickness=0,
			font='Courier',
			wrap=tk.WORD,
			state='disabled')
		self.infowin3.tag_config('normal', foreground='grey40')
		self.infowin3.tag_config('blue', foreground='blue')
		self.infowin3.tag_config('green', foreground='green')
		self.infowin3.tag_config('orange', foreground='orange')
		self.infowin3.tag_config('red', foreground='red')
		self.infowin3.grid(row=0, column=3, sticky='nsew')

		self.addresswin = tk.Text()
		self.addresswin.config(
			bg='black',
			fg='grey40',
			height=1,
			width=60,
			borderwidth=0,
			highlightthickness=0,
			font='Courier',
			wrap=tk.NONE,
			state='disabled')
		self.addresswin.tag_config('normal', foreground='grey40')
		self.addresswin.tag_config('blue', foreground='blue')
		self.addresswin.tag_config('red', foreground='red')
		self.addresswin.grid(row=1, column=1, columnspan=2, sticky='nsew')

		self.clockwin = tk.Text(self.root)
		self.clockwin.config(
			bg='black',
			fg='grey40',
			height=1,
			width=30,
			borderwidth=0,
			highlightthickness=0,
			font='Courier',
			state='disabled')
		self.clockwin.tag_config('green', foreground='green')
		self.clockwin.tag_config('orange', foreground='orange')
		self.clockwin.tag_config('red', foreground='red')
		self.clockwin.grid(row=1, column=3, sticky='nsew')

		self.msgwin = tk.Text(self.root)
		self.msgwin.config(
			bg='black',
			fg='paleturquoise1',
			height=30,
			width=108,
			borderwidth=0,
			highlightthickness=0,
			font='Courier',
			wrap=tk.WORD,
			state='disabled')
		self.msgwin.grid(row=2, column=0, columnspan=4, sticky='nsew')

		self.comwin = tk.Text(self.root)
		self.comwin.config(
			bg='black',
			fg='paleturquoise1',
			height=3,
			width=109,
			borderwidth=0,
			highlightthickness=0,
			font='Courier',
			wrap=tk.WORD,
			insertofftime=300,
			insertwidth=6,
			insertbackground='red')
		self.comwin.grid(row=3, column=0, columnspan=4, sticky='nsew')

		self.InfoRefresh()
		self.ClockMan(run=True)

		self.root.bind('<Configure>', self.OnResize)

		self.root.mainloop()


	def OnResize(self, event):
		self.ClockRefresh()


	def InfoRefresh(self, **kwargs):
		for kw in kwargs: self.info[kw] = kwargs[kw].split('$')

		self.infowin1.config(state='normal')
		self.infowin1.delete('1.0', tk.END)
		self.infowin1.insert('1.0', '\n\nMode:    \nName:    \nPhrase:  ')
		self.infowin1.insert('3.end', self.info['Mode'][0],
			self.info['Mode'][1])
		self.infowin1.insert('4.end', self.info['Name'][0],
			self.info['Name'][1])
		self.infowin1.insert('5.end', self.info['Phrase'][0],
			self.info['Phrase'][1])
		self.infowin1.config(state='disabled')

		self.addresswin.config(state='normal')
		self.addresswin.delete('1.0', tk.END)
		self.addresswin.insert('1.0', 'Address: ')
		self.addresswin.insert(tk.END, self.info['Address'][0],
			self.info['Address'][1])
		self.addresswin.config(state='disabled')

		self.infowin2.config(state='normal')
		self.infowin2.delete('1.0', tk.END)
		self.infowin2.insert('1.0',
			'\n\nRead/Write:  \nStatus:      \nBogeys:      ')
		self.infowin2.insert('3.end', self.info['Read/Write'][0],
			self.info['Read/Write'][1])
		self.infowin2.insert('4.end', self.info['Status'][0],
			self.info['Status'][1])
		self.infowin2.insert('5.end', self.info['Bogeys'][0],
			self.info['Bogeys'][1])
		self.infowin2.config(state='disabled')

		self.infowin3.config(state='normal')
		self.infowin3.delete('1.0', tk.END)
		self.infowin3.insert('1.0', 'Validated Parties:\n')
		for i in range(len(self.info['Parties'])):
			self.infowin3.insert(tk.END, self.info['Parties'][i], 'orange')
			if i != len(self.info['Parties'])-1:
				self.infowin3.insert(tk.END, ', ')
		self.infowin3.config(state='disabled')


	def ClockRefresh(self):
		[x,y,w,h] = self.root.grid_bbox(3, 1)
		baselen = tkf.Font(font='Courier').measure('Wait Time: [] 00:00')
		charlen = tkf.Font(font='Courier').measure('/')
		barlen = int((w - baselen)/charlen-1)
		nobars = int(barlen * self.clock['delta']/600)
		bar = '/'*nobars + '-'*(barlen - nobars)
		self.clockwin.config(state='normal')
		self.clockwin.delete('1.0', tk.END)
		self.clockwin.insert('1.0', 'Wait Time: [')
		for i in range(len(bar)):
			if i > int(barlen*.75):
				self.clockwin.insert(tk.END, bar[i], 'red')
			elif i > int(barlen*.50):
				self.clockwin.insert(tk.END, bar[i], 'orange')
			else:
				self.clockwin.insert(tk.END, bar[i], 'green')
		self.clockwin.insert(tk.END, '] ')
		if self.clock['status'] == 'running':
			self.clockwin.insert(tk.END, self.clock['time'], 'orange')
		else:
			self.clockwin.insert(tk.END, self.clock['time'], 'blue')
		self.clockwin.config(state='disabled')


	def ClockMan(self, run=None, reset=False):
		if run == True:
			self.clock['status'] = 'running'
			self.clock['starttime'] = time.time()
		elif run == False:
			self.clock['status'] = 'stopped'
		else:
			self.clock['delta'] = time.time() - self.clock['starttime']
			self.clock['time'] = '{0:02.0f}:{1:02.0f}'.format(*divmod(\
				self.clock['delta'], 60))
			self.ClockRefresh()
		if reset:
			self.clock = {'status': 'stopped', 'starttime': '', 'delta': 0,
				'time': '00:00'}
		if self.clock['status'] == 'running':
			self.root.after(1000, self.ClockMan)


## EXECUTABLE ## 

OTL()




