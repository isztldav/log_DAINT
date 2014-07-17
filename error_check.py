#!/usr/bin/env python
#
# Log parsing for crontab 
#
import smtplib
import time
from datetime import datetime, timedelta

# VARs
ADMINS = ["root"] # must be a list ex. ADMINS = ["root","admin"]
DAY = datetime.now().strftime("%Y%m%d")
ONEDAYAGO = int(DAY) - 1
NOW = datetime.now().strftime("%Y-%m-%dT%H:%M")
lastHourDateTime = datetime.now() - timedelta(hours = 1)
ONEHOURAGO = lastHourDateTime.strftime("%Y-%m-%dT%H:%M")
H = datetime.now().strftime("%H")
LOGDIR = "/home/isztld/Desktop/Log"

# Search for killed jobs in messages-* for the last hour


def send_email(SUBJECT,TEXT, TO):
	SERVER = "localhost"

	FROM = "daint@error"

	# Prepare actual message

	message = """\
	From: %s
	To: %s
	Subject: %s

	%s
	""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

	# Send the mail

	server = smtplib.SMTP(SERVER)
	server.sendmail(FROM, TO, message)
	server.quit()
	print "email sended!"

if str(H) <> "00":
	for line in open(LOGDIR + "/messages-" + DAY):
		parti = line.split(" ")
		data = parti[1].split(".")
		utile = data[0][:-3]
		data = utile.split("T")
		data[1] = data[1][3:]
		if data[0] == NOW[:-6] and data[1] == NOW[11:][:-3] or data[0] == ONEHOURAGO[:-6] and data[1] == ONEHOURAGO[11:][:-3]:
 			if "killed" in line:
  				send_email("DAINT: messages errors last hour", line, ADMINS)
else:
	for line in open(LOGDIR + "/messages-" + DAY):
		parti = line.split(" ")
		data = parti[1].split(".")
		utile = data[0][:-3]
		data = utile.split("T")
		data[1] = data[1][3:]
		if data[0] == NOW[:-6] and data[1] == NOW[11:][:-3] or data[0] == ONEHOURAGO[:-6] and data[1] == ONEHOURAGO[11:][:-3]:
 			if "killed" in line:
  				send_email("DAINT: messages errors last hour", line, ADMINS)
 
# Search for Xid & "Fallen of the bus" & "Lustre eviceted" errors
if str(H) <> "00":
	for line in open(LOGDIR + "/console-" + DAY):
		parti = line.split(" ")
		data = parti[0].split(".")
		utile = data[0][:-3]
		data = utile.split("T")
		data[1] = data[1][3:]
		if data[0] == NOW[:-6] and data[1] == NOW[11:][:-3] or data[0] == ONEHOURAGO[:-6] and data[1] == ONEHOURAGO[11:][:-3]:
			if "Xid" or "falle" or "evicted" in line:
				send_email("DAINT: console  errors last hour", line, ADMINS)
else:
	for line in open(LOGDIR + "/console-" + ONEDAYAGO):
		parti = line.split(" ")
		data = parti[0].split(".")
		utile = data[0][:-3]
		data = utile.split("T")
		data[1] = data[1][3:]
		if data[0] == NOW[:-6] and data[1] == NOW[11:][:-3] or data[0] == ONEHOURAGO[:-6] and data[1] == ONEHOURAGO[11:][:-3]:
			if "Xid" or "falle" or "evicted" in line:
				send_email("DAINT: console  errors last hour", line, ADMINS)
