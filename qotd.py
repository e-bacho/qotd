#!/usr/bin/python
# Licensed under the terms of the MIT License

# Setup
# 	pip install slackclient
# Copy your slack bot token into bot_token.txt
# Create quotes.csv file.

# Starting:
# python qotd.py

# Add bot to a channel by inviting it once you authorize the bot for your slack group.

import time
import datetime
import random
from slackclient import SlackClient

token = ""
botuid = '<@U1F54AWA3>: ' #  @qotd:

t = open('bot_token.txt','r')
token = t.read()

f = open('quotes.csv','r')
quotes = []
for line in f:
	quotes.append( line.split('|||')[0] )
f.close()	

f = open('attributions.csv','r')
attributions = []
for line in f:
	attributions.append( line.replace('\n','') )
f.close()	


#Slack formatting
#*bold* `code` _italic_ ~strike~

def addQuote(chan, msg):
	l = len(botuid) + 4
	q = msg['text'][l:].replace('"','')
	f = open('quotes.csv','a')
	f.write("\n" + q + '|||' + msg['user'] + '|||' + str(datetime.datetime.utcnow()))
	f.close()
	quotes.append(q)
	print sc.api_call('chat.postMessage', as_user='true', channel=chan, text='\t_*"' + q + '"*_\n\tQuote added. High Five <@' + msg['user'] + '>!')

def printQuote(chan, msg):
	print sc.api_call('chat.postMessage', as_user='true', channel=chan, text='\t' + random.choice(attributions) + ':\n\t\t_*"' + random.choice(quotes) + '"*_')

def listQuotes(chan, msg):
	mylist = '';
	for q in quotes:
		mylist += '\t_*' + q + '*_\n'
	print sc.api_call('chat.postMessage', as_user='true', channel=chan, text='\t' + mylist + '\n\n\t' + str(len(quotes)) + ' total quotes.')

def help(chan, msg):
	print sc.api_call('chat.postMessage', as_user='true', channel=chan, text=helptext + '.\n\t' + str(len(quotes)) + ' total quotes.')

commands = [
#{'command':botuid+'are you alive', 'response':'_*Yes, I\'m ALLLIIIVE*_'},
{'command':botuid+'quote', 'action':printQuote, 	'help':botuid+'quote [prints random quote], or by "lol"' },
{'command':botuid+'add',   'action':addQuote, 		'help':botuid+'add <some witty quote I want to add>' },
{'command':botuid+'list',  'action':listQuotes, 	'help':botuid+'list [prints out all quotes]' },
{'command':botuid+'help',  'action':help, 			'help':botuid+'help [this help text]'}
]

helptext = 'Greetings traveler! Commands are:\n'
for c in commands:
	helptext += "\t'" + c['help'] + "'\n"
commands[len(commands)-1]['response'] = helptext


def sendReply(chan, msg):
	if 'lol' in msg['text']:
		commands[0]['action'](chan, msg)
		return
		
	for command in commands:
		if command['command'] in msg['text']:
			command['action'](chan, msg)

sc = SlackClient(token)

if sc.rtm_connect():
    while True:
        messages = sc.rtm_read()
        #print messages
        for message in messages:
        	#print message
        	if 'type' in message and message['type'] == 'message' and 'bot_id' not in message and (botuid in message['text'] or 'lol' in message['text']):
        		print message
        		sendReply(message['channel'], message)
        time.sleep(1)
else:
    print "Connection Failed, invalid token?"
    
