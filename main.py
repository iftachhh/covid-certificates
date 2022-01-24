#!/usr/bin/env python3

from datetime import datetime
from json import load
from io import BytesIO
from flask import Flask, request, send_file
from signature import generate_keys, signing, verify, generateQR

app = Flask(__name__)
DATABASE = load(open('db.json'))
PRIVATE_KEY, PUBLIC_KEY = generate_keys(1024)

@app.route('/generate')
def generate():
	requested_user = request.args.get('id')
	if requested_user in DATABASE:
		response = {'ID':requested_user, **DATABASE[requested_user]}
		if datetime.strptime(response['expirationDate'], '%d/%m/%Y') < datetime.today().replace(hour=0, minute=0, second=0, microsecond=0):
			return '<br><h2 style="text-align: center; font-family: sans-serif;">ID is not eligible (expired)</h2>'
		response = signing(str(response), PRIVATE_KEY)
		if request.args.get('qr') == 'true':
			img_io = BytesIO()
			generateQR(response).save(img_io,'JPEG',quality=70)
			img_io.seek(0)
			return send_file(img_io, mimetype='image/jpeg')
		else: return response
	elif requested_user is None:
		return '<br><h2 style="text-align: center; font-family: sans-serif;">ID must be specified</h2>'
	elif not requested_user.isdigit() or len(requested_user)!=9:
		return '<br><h2 style="text-align: center; font-family: sans-serif;">ID is not valid</h2>'
	elif requested_user not in DATABASE:
		return '<br><h2 style="text-align: center; font-family: sans-serif;">ID is not eligible (don\'t exist)</h2>'
	else:
		return '<br><h2 style="text-align: center; font-family: sans-serif;">Unknown error occurred</h2>'

@app.errorhandler(404)
def errorhandler(error):
	return f'<br><h2 style="text-align: center; font-family: sans-serif;">This page doesn\'t exist</h2>',404

app.run()