#!/usr/bin/env python
#
# Log parsing for crontab 
#
import smtplib
import time
from datetime import datetime, timedelta

# VARs
##########		CONFIG
ADMINS = ["root"] # must be a list ex. ADMINS = ["root","admin"]
LOGDIR = "/home/support/Desktop/prova"
##########

# Day Vars
DAY = datetime.now().strftime("%Y%m%d")
ONEDAYAGO = int(DAY) - 1
NOW = datetime.now().strftime("%Y-%m-%dT%H:%M")
lastHourDateTime = datetime.now() - timedelta(hours = 1)
ONEHOURAGO = lastHourDateTime.strftime("%Y-%m-%dT%H:%M")
H = datetime.now().strftime("%H")
#Err vars
log=[]
n_err=0

def send_email(SUBJECT,TEXT, TO):
	SERVER = "localhost"

	FROM = "daint@error"
	msg=""
	# Prepare actual message
	for i in TEXT:
		msg=msg+i
	message = """\
From: %s
To: %s
Subject: %s

%s
	""" % (FROM, ", ".join(TO), SUBJECT, msg)

	# Send the mail

	server = smtplib.SMTP(SERVER)
	server.sendmail(FROM, TO, message)
	server.quit()
	print "email sended!"

def find_words(text, search):
	dSearch = {}
	dSearch = search.split()
	nt = len(text)
	for i in dSearch:
		for ii in range(0,nt):
			if i == text[ii]:
				return 1
	return 0

# Search for killed jobs in messages-* for the last hour
if str(H) <> "00":
	for line in open(LOGDIR + "/messages-" + DAY):
		parti = line.split(" ")
		data = parti[1].split(".")
		utile = data[0][:-3]
		data = utile.split("T")
		data[1] = data[1][:-3]
		if data[0] == NOW[:-6] and data[1] == NOW[11:][:-3] or data[0] == ONEHOURAGO[:-6] and data[1] == ONEHOURAGO[11:][:-3]:
 			if find_words(['killed'], line) == 1:
  				#send_email("DAINT: messages errors last hour", line, ADMINS)
  				log.append(line)
  				n_err+=1
else:
	for line in open(LOGDIR + "/messages-" + DAY):
		parti = line.split(" ")
		data = parti[1].split(".")
		utile = data[0][:-3]
		data = utile.split("T")
		data[1] = data[1][:3]
		if data[0] == NOW[:-6] and data[1] == NOW[11:][:-3] or data[0] == ONEHOURAGO[:-6] and data[1] == ONEHOURAGO[11:][:-3]:
 			if find_words(['killed'], line) == 1:
  				#send_email("DAINT: messages errors last hour", line, ADMINS)
  				log.append(line)
  				n_err+=1
if n_err <> 0:
	send_email("DAINT: messages errors last hour", log, ADMINS)
	n_err = 0

# Search for Xid & "Fallen of the bus" & "Lustre eviceted" errors
if str(H) <> "00":
	for line in open(LOGDIR + "/console-" + DAY):
		parti = line.split(" ")
		data = parti[0].split(".")
		utile = data[0][:-3]
		data = utile.split("T")
		data[1] = data[1][:-3]
		if data[0] == NOW[:-6] and data[1] == NOW[11:][:-3] or data[0] == ONEHOURAGO[:-6] and data[1] == ONEHOURAGO[11:][:-3]:
			if find_words(['Xid','falle','evicted'], line) == 1:
				#send_email("DAINT: console  errors last hour", line, ADMINS)
  				log.append(line)
  				n_err+=1
else:
	for line in open(LOGDIR + "/console-" + ONEDAYAGO):
		parti = line.split(" ")
		data = parti[0].split(".")
		utile = data[0][:-3]
		data = utile.split("T")
		data[1] = data[1][:-3]
		if data[0] == NOW[:-6] and data[1] == NOW[11:][:-3] or data[0] == ONEHOURAGO[:-6] and data[1] == ONEHOURAGO[11:][:-3]:
			if find_words(['Xid','falle','evicted'], line) == 1:
				#send_email("DAINT: console  errors last hour", line, ADMINS)
  				log.append(line)
  				n_err+=1

if n_err <> 0:
	send_email("DAINT: console  errors last hour", log, ADMINS)
	n_err = 0

exit()
