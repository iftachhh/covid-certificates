#!/usr/bin/env python3

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
import qrcode

def generate_keys(bits) -> tuple:
	PRIVATE_KEY = RSA.generate(1024)
	PUBLIC_KEY = PRIVATE_KEY.public_key()
	return PRIVATE_KEY, PUBLIC_KEY

def signing(unsigned_string, private_key) -> str:
	signed_string = SHA256.new(unsigned_string.encode())
	signed_string = PKCS1_v1_5.new(private_key).sign(signed_string)
	signed_string = b64encode(signed_string).decode()
	return '{} ={}'.format(unsigned_string,signed_string)

def verify(signed_string, public_key) -> bool:
	unsigned_string = SHA256.new(signed_string.split(' =')[0].encode())
	signed_string = b64decode(signed_string.split(' =')[1])
	is_verified = PKCS1_v1_5.new(public_key).verify(unsigned_string, signed_string)
	return is_verified

def generateQR(data) -> 'qrcode.image.pil.PilImage':
	qr = qrcode.QRCode()
	qr.add_data(data)
	qr.make()
	qr = qr.make_image(fill='black', back_color='white')
	return qr