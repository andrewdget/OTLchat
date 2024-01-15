## NOTES ##
'''
1. need to make work with windows paths
2. remember to remove hard coded test path
3. see what happens when you close the program but manualy delete a file...
4. need to add check path feature

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

import base64
import os
import datetime
import glob

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

## DEFINITIONS ##

class OTL:
	def __init__(self):

		self.info = {
			'Mode': ['Intranet Files', 'normal'],
			'Name': ['Not Set', 'blue'],
			'Phrase': ['Not Set', 'blue'],
			'Address': ['Not Set', 'blue'],
			'ReadWrite': ['Idle', 'normal'],
			'Status': ['Not Setup', 'blue'],
			'Bogeys': [0, 'green'],
			'Parties': []
			}
		self.clock = {'status': 'stopped', 'starttime': '', 'delta': 0,
		'time': '00:00'}
		self.keys = {'public_key': '', 'private_key': '', 'handshake_key': '',
			'salt': ''}
		self.prompt = '>>~~> '
		self.ephemera = []
		self.ignore = []
		self.messages = []
		self.handshakes = {}


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
		self.headerwin.config(bg='black', fg='orange', height=6, width=19,
			borderwidth=0, highlightthickness=0, state='disabled')
		self.headerwin.grid(row=0, column=0, rowspan=2, padx=5, sticky='nsew')

		self.infowin1 = tk.Text(self.root)
		self.infowin1.config(bg='black', fg='grey40', height=5, width=30,
			borderwidth=0, highlightthickness=0, font='Courier', wrap=tk.NONE,
			state='disabled')
		self.infowin1.tag_config('normal', foreground='grey40')
		self.infowin1.tag_config('blue', foreground='blue')
		self.infowin1.tag_config('green', foreground='green')
		self.infowin1.tag_config('orange', foreground='orange')
		self.infowin1.tag_config('red', foreground='red')
		self.infowin1.grid(row=0, column=1, sticky='nsew')

		self.infowin2 = tk.Text(self.root)
		self.infowin2.config(bg='black', fg='grey40', height=5, width=30, 
			borderwidth=0, highlightthickness=0, font='Courier', wrap=tk.NONE,
			state='disabled')
		self.infowin2.tag_config('normal', foreground='grey40')
		self.infowin2.tag_config('blue', foreground='blue')
		self.infowin2.tag_config('green', foreground='green')
		self.infowin2.tag_config('orange', foreground='orange')
		self.infowin2.tag_config('red', foreground='red')
		self.infowin2.grid(row=0, column=2, sticky='nsew')

		self.infowin3 = tk.Text(self.root)
		self.infowin3.config(bg='black', fg='grey40', height=5, width=30,
			borderwidth=0, highlightthickness=0, font='Courier', wrap=tk.WORD,
			state='disabled')
		self.infowin3.tag_config('normal', foreground='grey40')
		self.infowin3.tag_config('blue', foreground='blue')
		self.infowin3.tag_config('green', foreground='green')
		self.infowin3.tag_config('orange', foreground='orange')
		self.infowin3.tag_config('red', foreground='red')
		self.infowin3.grid(row=0, column=3, sticky='nsew')

		self.addresswin = tk.Text()
		self.addresswin.config(bg='black', fg='grey40', height=1, width=60,
			borderwidth=0, highlightthickness=0, font='Courier', wrap=tk.NONE,
			state='disabled')
		self.addresswin.tag_config('normal', foreground='grey40')
		self.addresswin.tag_config('blue', foreground='blue')
		self.addresswin.tag_config('red', foreground='red')
		self.addresswin.grid(row=1, column=1, columnspan=2, sticky='nsew')

		self.clockwin = tk.Text(self.root)
		self.clockwin.config(bg='black', fg='grey40', height=1, width=30,
			borderwidth=0, highlightthickness=0, font='Courier',
			state='disabled')
		self.clockwin.tag_config('green', foreground='green')
		self.clockwin.tag_config('orange', foreground='orange')
		self.clockwin.tag_config('red', foreground='red')
		self.clockwin.grid(row=1, column=3, sticky='nsew')

		self.msgwin = tk.Text(self.root)
		self.msgwin.config(bg='black', fg='paleturquoise1', height=30,
			width=108, borderwidth=0, highlightthickness=0, font='Courier',
			wrap=tk.WORD, state='disabled')
		self.msgwin.grid(row=2, column=0, columnspan=4, sticky='nsew')

		self.comwin = tk.Text(self.root)
		self.comwin.config(bg='black', fg='paleturquoise1', height=3, width=109,
			borderwidth=0, highlightthickness=0, font='Courier', wrap=tk.WORD,
			insertofftime=300, insertwidth=6, insertbackground='red')
		self.comwin.tag_config('red', foreground='red')
		self.comwin.grid(row=3, column=0, columnspan=4, padx=5, sticky='nsew')

		self.comwin.focus_set()
		self.InfoRefresh()
		self.PromptRefresh()
		self.GenRSAKeys()

		self.root.bind('<Configure>', self.OnResize)
		self.comwin.bind('<FocusOut>', self.FocusReturn)
		self.comwin.bind('<KeyRelease>', self.PromptProtect)
		self.comwin.bind('<Key>', self.HidePhrase)
		self.comwin.bind('<Return>', self.ComReturn)
		self.comwin.bind('<Destroy>', self.OnDestroy)

		self.root.mainloop()


	def PromptRefresh(self):
		lock = False
		self.comwin.delete('1.0', tk.END)
		if self.info['Name'][0] == 'Not Set': self.prompt = 'Name >> '
		elif self.info['Phrase'][0] == 'Not Set': self.prompt = 'Phrase >> '
		elif self.info['Address'][0] == 'Not Set': self.prompt = 'Address >> '
		elif len(list(self.handshakes.keys())) == 0:
			self.prompt = 'Pre-Contact - WAITING'
			lock = True
		elif len(list(self.handshakes.keys())) != 0:
			for user in list(self.handshakes.keys()):
				if self.handshakes[user][1] == False:
					self.prompt = 'User ' + user + \
					' Authenticated. Establish Encrypted Channel? (y/n) '
		else:
			self.prompt = '>>~~> '
		self.PromptProtect(lock=lock)


	def PromptProtect(self, event=None, lock=False):
		[line, column] = self.comwin.index(tk.INSERT).split('.')
		if int(line) == 1:
			if int(column) < len(self.prompt):
				self.comwin.delete('1.0', '1.' + str(len(self.prompt)))
				self.comwin.insert('1.0', self.prompt, 'red')
				if lock: self.comwin.config(state='disabled')

	def HidePhrase(self, event):
		if self.prompt == 'Phrase >> ':
			if self.info['Phrase'][0] == 'Not Set':
				self.info['Phrase'][0] = ''
			self.info['Phrase'][0] += event.char
			prompt_index = '1.' + str(len(self.prompt))
			self.comwin.delete(prompt_index, tk.END)
			self.comwin.insert(prompt_index, '*'*len(self.info['Phrase'][0]))
			return 'break'


	def ComReturn(self, event):
		msg = self.comwin.get('1.' + str(len(self.prompt)), tk.END).strip()
		if self.prompt == 'Name >> ':
			self.InfoRefresh(Name=msg + '$normal')
		elif self.prompt == 'Phrase >> ':
			self.InfoRefresh(Phrase=msg + '$normal')
		elif self.prompt == 'Address >> ':
			msg = '/Users/agetman/desktop/tets'
			self.InfoRefresh(Status = 'Pre-Contact$orange',
				Address=msg + '$normal')
			self.ClockMan(run=True)
			self.GenHandshakeKey()
			handshake = self.Solicit()
			self.ephemera.append(handshake)
			self.ignore.append(handshake)
			self.Check4Packets()
		self.PromptRefresh()
		return 'break'


	def Check4Packets(self):
		'''
		self.ephemera = []
		self.ignore = []
		self.messages = []
		self.Handshakes = {}
		'''
		self.InfoRefresh(ReadWrite='Active$blue')
		self.infowin3.update()
		rootdir = os.getcwd()
		os.chdir(self.info['Address'][0])
		files = sorted(glob.glob('*.txt'), key=lambda x: x.replace('-', '.'))
		for file in files:
			if file not in self.ignore:
				self.ignore.append(file)
				try:
					with open(file, 'rb') as f:
						packet = f.read()
				except: pass

				try:
					self.AuthenticateHandshake(packet)
					self.PromptRefresh()
				except: self.info['Bogeys'] = [self.info['Bogeys'][0]+1, 'orange']


		os.chdir(rootdir)
		self.InfoRefresh(ReadWrite='Idle$normal')
		self.root.after(2000, self.Check4Packets)







	def OnResize(self, event):
		self.ClockRefresh()


	def FocusReturn(self, event): self.comwin.focus_set()


	def OnDestroy(self, event):
		rootdir = os.getcwd()
		if self.info['Address'][0] != 'Not Set':
			os.chdir(self.info['Address'][0])
			for file in self.ephemera:
				try:
					os.remove(file)
				except: pass
			os.chdir(rootdir)


	def GenRSAKeys(self):
		self.keys['private_key'] = rsa.generate_private_key(\
			public_exponent=65537, key_size=2048)
		self.keys['public_key'] = self.keys['private_key'].public_key()\
			.public_bytes(encoding=serialization.Encoding.PEM,
				format=serialization.PublicFormat.SubjectPublicKeyInfo)

	def GenHandshakeKey(self):
		date = datetime.datetime.now()
		front = str(date.year).encode('utf-8')
		midle = b'\x89\x8dE\x7f\xf1k\x83\t?\xb9\xc3\xa4\xb6\xc9'
		end = '{0:02.0f}{1:02.0f}'.format(date.month, date.day).encode('utf-8')
		self.keys['salt'] = front + midle + end
		kdf = PBKDF2HMAC(algorithm = hashes.SHA256(), length = 32,
			salt = self.keys['salt'], iterations = 480000)
		self.keys['handshake_key'] = base64.urlsafe_b64encode(\
			kdf.derive(self.info['Phrase'][0].encode('utf-8')))

	def Solicit(self):
		handshake = self.info['Name'][0].encode('utf-8') + b':$:'\
			+ self.keys['salt'] + b':$:' + self.keys['public_key']
		packet = Fernet(self.keys['handshake_key']).encrypt(handshake)

		rootdir = os.getcwd()
		os.chdir(self.info['Address'][0])
		filename = str(time.time()).replace('.', '-') + '.txt'
		with open(filename, 'wb') as f:
			f.write(packet)
		os.chdir(rootdir)
		return filename


	def AuthenticateHandshake(self, packet): 
		handshake = Fernet(self.keys['handshake_key']).decrypt(packet).split(b':$:')
		if handshake[1] == self.keys['salt']:
			name = handshake[0].decode('utf-8')
			public_key = handshake[2]
			self.handshakes[name] = [public_key, False]
		else:
			self.info['Bogeys'] = [self.info['Bogeys'][0]+1, 'orange']

















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
		self.infowin2.insert('3.end', self.info['ReadWrite'][0],
			self.info['ReadWrite'][1])
		self.infowin2.insert('4.end', self.info['Status'][0],
			self.info['Status'][1])
		self.infowin2.insert('5.end', self.info['Bogeys'][0],
			self.info['Bogeys'][1])
		self.infowin2.config(state='disabled')

		self.infowin3.config(state='normal')
		self.infowin3.delete('1.0', tk.END)
		self.infowin3.insert('1.0', 'Parties Present:\n')
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
			self.clockwin.insert(tk.END, self.clock['time'])
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



