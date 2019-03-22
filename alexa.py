from py_irsend import irsend

#print(irsend.list_remotes())
#print(irsend.list_codes('/home/pi/testlirc.conf'))
#irsend.send_once('/home/pi/testlirc.conf', ['KEY_POWER'])


from flask import Flask
from flask_ask import Ask, statement, convert_errors
import logging

app = Flask(__name__)
ask = Ask(app, '/')

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.intent('switchtv', mapping={'code': 'code'})
def switchtvcode(code):

    if code in ['on', 'off']:	irsend.send_once('/home/pi/testlirc.conf', ['KEY_POWER'])

    return statement('turning tv {}'.format(code))

@ask.intent('volume', mapping={'incrdecr': 'incrdecr','number': 'number'})
def volume(incrdecr,number):
    try:
        pinNum = int(number)
    except Exception as e:
        return statement('Number not valid.')

    print("num is {}".format(number))

    if incrdecr == 'increase':
	type = 'KEY_VOLUMEUP'
	state = 'increasing'
    else:
	type = 'KEY_VOLUMEDOWN'
	state = 'decreasing'

    for i in range(int(number)):
	irsend.send_once('/home/pi/testlirc.conf', [type])

    return statement("{} volume by {}".format(state,number))

if __name__ == '__main__':
    app.run(debug=True)
