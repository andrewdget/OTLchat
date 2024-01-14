## NOTES ##
'''
1. add check path for address
'''



## DEPENDENCIES ## 

import tkinter as tk
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
			'Status': ['Not Setup', 'orange'],
			'Bogeys': ['0', 'green'],
			'Parties': []
			}

		self.root = tk.Tk()
		self.root.title('OTL')
		self.root.configure(bg='blue')

		self.root.columnconfigure(0, weight=0)
		self.root.columnconfigure(1, weight=0)
		self.root.columnconfigure(2, weight=0)
		self.root.columnconfigure(3, weight=1)
		self.root.rowconfigure(0, weight=0)
		self.root.rowconfigure(1, weight=0)
		self.root.rowconfigure(2, weight=1)
		self.root.rowconfigure(3, weight=0)

		self.headerwin = tk.Text(self.root)
		self.headerwin.insert('1.0', '\n' + pyfiglet.figlet_format('OTL', font = 'slant'))
		self.headerwin.config(
			height=6,
			width=19,
			borderwidth=0,
			highlightthickness=0,
			state='disabled',
			bg='blue')
		self.headerwin.grid(row=0, column=0, rowspan=2, padx=5, sticky='nsew')

		self.infowin1 = tk.Text(self.root)
		self.infowin1.config(
			height=5,
			width=30,
			borderwidth=0,
			highlightthickness=0,
			state='disabled',
			bg='green')
		self.infowin1.tag_config('normal', foreground='grey40')
		self.infowin1.tag_config('blue', foreground='blue')
		self.infowin1.tag_config('green', foreground='green')
		self.infowin1.tag_config('orange', foreground='orange')
		self.infowin1.tag_config('red', foreground='red')
		self.infowin1.grid(row=0, column=1, sticky='nsew')

		self.infowin2 = tk.Text(self.root)
		self.infowin2.config(
			height=5,
			width=30, 
			borderwidth=0,
			highlightthickness=0,
			state='disabled',
			bg='orange')
		self.infowin2.tag_config('normal', foreground='grey40')
		self.infowin2.tag_config('blue', foreground='blue')
		self.infowin2.tag_config('green', foreground='green')
		self.infowin2.tag_config('orange', foreground='orange')
		self.infowin2.tag_config('red', foreground='red')
		self.infowin2.grid(row=0, column=2, sticky='nsew')

		self.infowin3 = tk.Text(self.root)
		self.infowin3.config(
			height=5,
			width=30,
			borderwidth=0,
			highlightthickness=0,
			state='disabled',
			bg='yellow')
		self.infowin3.tag_config('normal', foreground='grey40')
		self.infowin3.tag_config('blue', foreground='blue')
		self.infowin3.tag_config('green', foreground='green')
		self.infowin3.tag_config('orange', foreground='orange')
		self.infowin3.tag_config('red', foreground='red')
		self.infowin3.grid(row=0, column=3, sticky='nsew')

		self.addresswin = tk.Text()
		self.addresswin.config(
			height=1,
			width=60,
			borderwidth=0,
			highlightthickness=0,
			state='disabled',
			bg='pink')
		self.addresswin.tag_config('normal', foreground='grey40')
		self.addresswin.tag_config('blue', foreground='blue')
		self.addresswin.tag_config('red', foreground='red')
		self.addresswin.grid(row=1, column=1, columnspan=2, sticky='nsew')

		self.clockwin = tk.Text(self.root)
		self.clockwin.config(
			height=1,
			width=30,
			borderwidth=0,
			highlightthickness=0,
			state='disabled',
			bg='purple')
		self.clockwin.grid(row=1, column=3, sticky='nsew')

		self.msgwin = tk.Text(self.root)
		self.msgwin.config(
			height=30,
			width=108,
			borderwidth=0,
			highlightthickness=0,
			state='disabled',
			bg='grey')
		self.msgwin.grid(row=2, column=0, columnspan=4, sticky='nsew')

		self.comwin = tk.Text(self.root)
		self.comwin.config(
			height=3,
			width=109,
			borderwidth=0,
			highlightthickness=0,
			bg='teal')
		self.comwin.grid(row=3, column=0, columnspan=4, sticky='nsew')

		self.InfoRefresh()

		self.root.mainloop()


	def InfoRefresh(self, **kwargs):
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

		self.info = {
			'Mode': ['Intranet Files', 'normal'],
			'Name': ['Not Set', 'blue'],
			'Phrase': ['Not Set', 'blue'],
			'Address': ['Not Set', 'blue'],
			'Read/Write': False,
			'Status': ['Not Setup', 'orange'],
			'Bogeys': ['0', 'green'],
			'Parties': []
			}
		'''

		for kw in kwargs: self.info[kw] = kwargs[kw].split('$')

		self.infowin1.config(state='normal')
		self.infowin1.delete('1.0', tk.END)
		self.infowin1.insert('1.0', '\n\nMode:    \nName:    \nPhrase:  ')
		self.infowin1.insert('3.end', self.info['Mode'][0], self.info['Mode'][1])
		self.infowin1.insert('4.end', self.info['Name'][0], self.info['Name'][1])
		self.infowin1.insert('5.end', self.info['Phrase'][0], self.info['Phrase'][1])
		self.infowin1.config(state='disabled')

		self.addresswin.config(state='normal')
		self.addresswin.delete('1.0', tk.END)
		self.addresswin.insert('1.0', 'Address: ')
		self.addresswin.insert(tk.END, self.info['Address'][0], self.info['Address'][1])
		self.addresswin.config(state='disabled')

		self.infowin2.config(state='normal')
		self.infowin2.delete('1.0', tk.END)
		self.infowin2.insert('1.0', '\n\nRead/Write:  \nStatus:      \nBogeys:      ')
		self.infowin2.insert('3.end', self.info['Read/Write'][0], self.info['Read/Write'][1])
		self.infowin2.insert('4.end', self.info['Status'][0], self.info['Status'][1])
		self.infowin2.insert('5.end', self.info['Bogeys'][0], self.info['Bogeys'][1])
		self.infowin2.config(state='disabled')

		self.infowin3.config(state='normal')
		self.infowin3.delete('1.0', tk.END)
		self.infowin3.insert('1.0', 'Validated Parties:\n')
		for party in self.info['Parties']:
			self.infowin3.insert(tk.END, party + ', ', 'orange')
		self.infowin3.config(state='disabled')

## EXECUTABLE ## 

OTL()


