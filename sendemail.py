#!/usr/bin/python
#coding: utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os
import sys
from ConfigParser import ConfigParser
class SendEmail(object):
	def __init__(self):
		config_file = sys.path[0] + os.path.sep +'mail.conf'
		conf = ConfigParser()
		conf.read(config_file)
		self.mail_host = conf.get('server','host')
		self.mail_user = conf.get('client','account')
		self.mail_pass = conf.get('client','passwd')
		name = conf.get('client','name')
		try:
			self.address = conf.get('client','address')
		except:
			self.address = mail_user + '@' + mail_host[5:]
		self.me = name + '<' + self.address + '>'

	def _build_msg(self,args):
		to_list = args['t']
		msg = MIMEMultipart()
		msg['From'] = self.me
		msg['Subject'] = args['s']
		msg['To'] = ';'.join(to_list)
		msg.attach(MIMEText(args['m'], 'plain','utf-8'))
		for file in args['f']:
			part = MIMEBase('application','octet-stream')
			part.set_payload(open(file,'rb').read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', 'attachment; filename="%s"' %os.path.basename(file))
			msg.attach(part)
		return msg

	def send(self,args):
		msg = self._build_msg(args)
		send_smtp = smtplib.SMTP()
		send_smtp.connect(self.mail_host)
		send_smtp.login(self.mail_user,self.mail_pass)
		send_smtp.sendmail(self.address,args['t'],msg.as_string())
		send_smtp.close()

if __name__ == '__main__':
	argv = sys.argv
	argv.pop(0)
	args = {'t':[],'m':'','s':'','f':[]}
	for item in argv:
		if item[0] == '-':
			flag = item[1]
			continue
		if isinstance(args[flag],list):
			args[flag].append(item)
		else:
			args[flag] += item
	SendEmail().send(args)
	print u'发送成功'
