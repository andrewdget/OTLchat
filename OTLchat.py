## NOTES ##
'''
2. need to make work with windows paths
3. remember to remove hard coded test path

1. send out handshake salt encrypted with house salt
	2. send out messages as normal
3. look for other handshakes
	4. decrypt messages acordingly
5. delete own messages and handshakes when closed. 

6. see what happens when you close the program but manualy delete a file...
'''

## DEPENDENCIES ## 

import base64
import os
import time
import glob

import tkinter as tk
import pyfiglet

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

## DEFINITIONS ##

def genkey(phrase):
	kdf = PBKDF2HMAC(
		algorithm = hashes.SHA256(),
		length = 32,
		salt = b'\x89\x8dE\x7f\xf1k\x83\t?\xb9\xc3\xa4\xb6\xc9\xcf\xb5',
		iterations = 480000
		)
	return base64.urlsafe_b64encode(kdf.derive(phrase.encode('utf-8')))


def forward(msg, key):
	return Fernet(key).encrypt(msg.encode('utf-8'))


def backward(packet, key):
	return Fernet(key).decrypt(packet).decode('utf-8')


def deliver(phrase, name, msg, address):
	packet = forward(name + ': ' + msg, genkey(phrase))
	rootdir = os.getcwd()
	os.chdir(address)
	filename = str(time.time()).replace('.', '-') + '.txt'
	with open(filename, 'wb') as f:
		f.write(packet)
	os.chdir(rootdir)
	return filename


def retrieve(phrase, address, ignore=[]):
	rootdir = os.getcwd()
	os.chdir(address)
	stale = []
	bundle = []
	for file in sorted(glob.glob('*.txt'), key=lambda x: x.replace('-', '.')):
		try:
			if file not in ignore:
				stale.append(file)
				with open(file, 'rb') as f:
					bundle.append(backward(f.read(), genkey(phrase)))
		except:
			pass
	os.chdir(rootdir)
	return stale, bundle


class OTL:
	def __init__(self):

		self.name = None
		self.phrase = None
		self.address = None
		self.ready = False

		self.handshakes = []
		self.ignore = []
		self.ephemera = []
		self.messages = []

		self.root = tk.Tk()
		self.root.title('OTL')
		self.root.configure(bg='black')

		self.root.columnconfigure(0, weight=0)
		self.root.columnconfigure(1, weight=1)
		self.root.rowconfigure(0, weight=0)
		self.root.rowconfigure(1, weight=1)
		self.root.rowconfigure(2, weight=0)

		self.header = tk.Text(self.root)
		self.header.insert('1.0', pyfiglet.figlet_format('OTL', font = 'slant'))
		self.header.config(bg='black', fg='orange', borderwidth=0,
			highlightthickness=0, padx=10, height=6, width=20, state='disabled')
		self.header.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

		self.infowin = tk.Text(self.root)
		self.infowin.config(bg='black', fg='grey40', borderwidth=0,
			highlightthickness=0, heigh=6, font='Courier', state='disabled')
		self.infowin.tag_config('green', foreground='green')
		self.infowin.tag_config('blue', foreground='blue')
		self.infowin.tag_config('red', foreground='red')
		self.infowin.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

		self.msgwin = tk.Text(self.root)
		self.msgwin.config(bg='black', fg='paleturquoise1', borderwidth=0,
			highlightthickness=0, height=40, width=75, font='Courier',
			wrap=tk.WORD, state='disabled')
		self.msgwin.tag_config('self', foreground='mediumpurple2')
		self.msgwin.tag_config('other', foreground='seagreen1')
		self.msgwin.grid(row=1, column=0, columnspan=2, padx=5, pady=5,
			sticky='nsew')

		self.comwin = tk.Text(self.root)
		self.comwin.config(bg='black', fg='paleturquoise1', borderwidth=0,
			highlightthickness=0, height=3, width=75, font='Courier',
			wrap=tk.WORD, insertofftime=300, insertwidth=6,
			insertbackground='red3', padx=5)
		self.comwin.tag_config('prompt', foreground='red3')
		self.comwin.grid(row=2, column=0, columnspan=2, padx=5, pady=5,
			sticky='nsew')

		self.comwin.focus_set()
		self.InfoRefresh('not ready', 'red')
		self.PromptMan()
		self.Check4Bundles()
		
		self.comwin.bind('<FocusOut>', self.FocusReturn)
		self.comwin.bind('<KeyRelease>', self.PromptProtect)
		self.comwin.bind('<Key>', self.HidePhrase)
		self.comwin.bind('<Return>', self.ComReturn)
		self.comwin.bind('<Destroy>', self.OnDestroy)

		self.root.mainloop()


	def OnDestroy(self, event):
		rootdir = os.getcwd()
		os.chdir(self.address)
		for file in self.ephemera:
			os.remove(file)
		os.chdir(rootdir)


	def InfoRefresh(self, status, tag):
		self.infowin.config(state='normal')
		self.infowin.delete('1.0', tk.END)
		self.infowin.insert('1.0', '\nName:    ' + str(self.name) + '\n')
		if self.phrase == None:
			self.infowin.insert(tk.END, 'Phrase:  ' + str(self.phrase) + '\n')
		else:
			self.infowin.insert(tk.END, 'Phrase:  ' + '*' * len(self.phrase) + '\n')
		self.infowin.insert(tk.END, 'Address: ' + str(self.address) + '\n')
		self.infowin.insert(tk.END, 'Status:  ')
		self.infowin.insert(tk.END, status, tag)
		self.infowin.config(state='disabled')
		self.infowin.update()


	def PromptMan(self):
		self.comwin.delete('1.0', tk.END)
		if self.name == None:
			self.prompt = 'Name >> '
		elif self.phrase == None:
			self.prompt = 'Phrase >> '
		elif self.address == None:
			self.prompt = 'Address >> '
		else:
			self.prompt = '>>~~> '
		self.prompt_lim = '1.' + str(len(self.prompt))
		self.comwin.insert('1.0', self.prompt, 'prompt')


	def FocusReturn(self, event):
		self.comwin.focus_set()


	def HidePhrase(self, event):
		if self.prompt == 'Phrase >> ':
			if self.phrase == None:
				self.phrase = ''
			self.phrase += event.char
			self.comwin.delete(self.prompt_lim, tk.END)
			self.comwin.insert(self.prompt_lim, '*'*len(self.phrase))
			return 'break'


	def PromptProtect(self, event):
		cursor_position = self.comwin.index(tk.INSERT)
		[cursor_line, cursor_column] = cursor_position.split('.')
		if int(cursor_line) == 1:
			if int(cursor_column) < 10:
				self.comwin.delete('1.0', self.prompt_lim)
				self.comwin.insert('1.0', self.prompt, 'prompt')


	def ComReturn(self, event):
		msg = self.comwin.get(self.prompt_lim, tk.END).replace('\n', '')
		if self.prompt == 'Name >> ':
			self.name = msg
			self.InfoRefresh('not ready', 'red')
		elif self.prompt == 'Phrase >> ':
			self.phrase = msg
			self.InfoRefresh('not ready', 'red')
		elif self.prompt == 'Address >> ':
			self.address = msg
			self.address = '/Users/agetman/desktop/tets'
			self.ready = True
			self.InfoRefresh('ready', 'green')
		else:
			if len(msg) != 0:
				self.InfoRefresh('sending', 'blue')
				try:
					self.ephemera.append(deliver(self.phrase, self.name, msg,\
						self.address))
				except:
					self.InfoRefresh('send failed', 'red')
				else:
					self.InfoRefresh('ready', 'green')
		self.PromptMan()
		return 'break'


	def Check4Bundles(self):
		if self.ready:
			self.InfoRefresh('retrieving', 'blue')
			[stale, bundle] = retrieve(self.phrase, self.address, self.ignore)
			self.ignore.extend(stale)
			if len(bundle) != 0:
				self.msgwin.config(state='normal')
				for msg in bundle:
					[name, content] = msg.split(': ')
					if name == self.name:
						self.msgwin.insert(tk.END, name + ': ', 'self')
					else:
						self.msgwin.insert(tk.END, name + ': ', 'other')
					self.msgwin.insert(tk.END, content + '\n')
				self.msgwin.config(state='disabled')
			self.InfoRefresh('ready', 'green')

		self.root.after(2000, self.Check4Bundles)

## EXECUTABLE ## 

OTL()
