
import base64
import os
import time
import datetime
import glob

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def GenRSAKeys():
	private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
	public_key = private_key.public_key().public_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PublicFormat.SubjectPublicKeyInfo
		)
	return private_key, public_key

def GenHandshakeKey(phrase):
	date = datetime.datetime.now()
	front = str(date.year).encode('utf-8')
	midle = b'\x89\x8dE\x7f\xf1k\x83\t?\xb9\xc3\xa4\xb6\xc9'
	end = '{0:02.0f}{1:02.0f}'.format(date.month, date.day).encode('utf-8')
	salt = front + midle + end
	kdf = PBKDF2HMAC(algorithm = hashes.SHA256(), length = 32,
		salt = salt, iterations = 480000)
	handshake_key = base64.urlsafe_b64encode(kdf.derive(phrase.encode('utf-8')))
	return handshake_key, salt

def Solicit(handshake_key, salt, public_key, name, address):
	handshake = name.encode('utf-8') + b':$:' + salt + b':$:' + public_key
	packet = Fernet(handshake_key).encrypt(handshake)

	rootdir = os.getcwd()
	os.chdir(address)
	filename = str(time.time()).replace('.', '-') + '.txt'
	with open(filename, 'wb') as f:
		f.write(packet)
	os.chdir(rootdir)
	return filename

def ValidateHandshake(packet, handshake_key, salt):
	handshake = Fernet(handshake_key).decrypt(packet).split(b':$:')
	if handshake[1] == salt:
		name = handshake[0].decode('utf-8')
		public_key = handshake[2]
		return name, public_key
	else:
		return 'Bogey', None

def Retrieve(private_key, handshake_key, salt, address, ignore=[]):
	rootdir = os.getcwd()
	os.chdir(address)
	stale = []
	for file in sorted(glob.glob('*.txt'), key=lambda x: x.replace('-', '.')):
		if file not in ignore:
			stale.append(file)
			try:
				with open(file, 'rb') as f:
					packet = f.read()
			except: pass

			try:
				[name, public_key] = ValidateHandshake(packet, handshake_key, salt)
				print(name)
			except:
				try:
					plaintext = RSAdecrypt(private_key, packet)
					print(plaintext)
				except:
					pass


def RSAsend(public_key, name, msg, address):
	plaintext = name + ': ' + msg
	pad = padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
				algorithm=hashes.SHA256(), label=None)
	loaded_public_key = serialization.load_pem_public_key(public_key)
	packet = loaded_public_key.encrypt(plaintext.encode('utf-8'), pad)

	rootdir = os.getcwd()
	os.chdir(address)
	filename = str(time.time()).replace('.', '-') + '.txt'
	with open(filename, 'wb') as f:
		f.write(packet)
	os.chdir(rootdir)
	return filename

def RSAdecrypt(private_key, packet):
	pad = padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
		algorithm=hashes.SHA256(), label=None)
	plaintext = private_key.decrypt(packet, pad).decode('utf-8')
	print(plaintext)



[private_key, public_key] = GenRSAKeys()
[handshake_key, salt] = GenHandshakeKey('test')

Solicit(handshake_key, salt, public_key, 'usher', '/Users/agetman/desktop/tets')
Solicit(handshake_key, salt, public_key, 'fox', '/Users/agetman/desktop/tets')
Retrieve(private_key, handshake_key, salt, '/Users/agetman/desktop/tets')

RSAsend(public_key, 'usher', 'hello world', '/Users/agetman/desktop/tets')

Retrieve(private_key, handshake_key, salt, '/Users/agetman/desktop/tets')



