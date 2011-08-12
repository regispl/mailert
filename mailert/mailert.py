import smtplib

from email.MIMEText import MIMEText
from pprint import pprint

class MailertException(Exception): pass
class RequiredParameterMissingException(MailertException): pass
class InvalidConnectionStringFormat(MailertException): pass

class Mailert(object):

	# If one of them is missing in constructor an exception will be raised
	OBLIGATORY_PARAMETERS = ['host', 'user', 'password', 'service', 'receivers']

	MISSING_PARAMETER_INFO = 'Parameter %s is missing!'
	WRONG_FORMAT_INFO = 'Connection string should look like: user:password@host[:port].'

	subject_format = '[%(level)s] %(service)s - %(subject)s'

	conn = None
	config = dict()

	def __init__(self, **kwargs):
		"""
		Mailert initialization. Available options:
		
		host 		- SMTP host,
		port 		- SMTP port (optional),
		ssl 		- Use SSL (True/False),
		timeout 	- SMTP timeout (optional),
		user 		- SMTP user,
		password 	- SMTP password,
		keep_alive 	- Decides if connection should be closed after sending an 
						e-mail or not (optional; default True, requires closing 
						the connection manually),
		service 	- Name of the monitored service - it will be displayed in 
						title of the mail,
		sender 		- Common name of the mail sender (optional; if empty, 'user' 
						field will be used),
		receivers  	- List of alert receivers,
		connstr 	- Connection string for easier parameter passing. Format: 
						user:password@host[:port]. IMPORTANT! None of the fields 
						can contain '@' and ':'. Hopefully it will be fixed 
						someday to allow logins with '@'.
		"""

		args = kwargs.copy()

		if 'connstr' in args:
			connstr = args['connstr']
			if '@' in connstr:
				user_password, host_port = connstr.split('@')				
				if ':' in user_password:
					args['user'], args['password'] = user_password.split(':')
				else:
					raise InvalidConnectionStringFormat, self.WRONG_FORMAT_INFO
				if ':' in host_port:
					host, port = host_port.split(':')
				else:
					host = host_port
					port = None
				args['host'], args['port'] = host, port
			else:
				raise InvalidConnectionStringFormat, self.WRONG_FORMAT_INFO

		self._check_if_parameters_are_missing(args)

		self.config['host'] = args['host']
		self.config['user'] = args['user']
		self.config['password'] = args['password']
		self.config['service'] = args['service']
		self.config['receivers'] = args['receivers']

		if 'port' in args:
			self.config['port'] = args['port'] 

		if 'ssl' in args:
			self.config['ssl'] = args['ssl'] 

		if 'timeout' in args:
			self.config['timeout'] = args['timeout'] 

		self.config['keep_alive'] = True
		if 'keep_alive' in args:
			self.config['keep_alive'] = args['keep_alive'] 

		if 'sender' in args:
			self.config['sender'] = args['sender'] 

	def __del__(self):
		if self.conn is not None:
			self.conn.quit()

	def _check_if_parameters_are_missing(self, params):
		for key in self.OBLIGATORY_PARAMETERS:
			if key not in params:
				raise RequiredParameterMissingException, self.MISSING_PARAMETER_INFO % key

	def _send_alert(self, loglevel, subject, body, **kwargs):
		c = self.config

		if not self.conn:
			constructor = smtplib.SMTP if c.get('ssl', None) in [None, False] else smtplib.SMTP_SSL
			self.conn = constructor(c['host'], c['port'])
			self.conn.login(c['user'], c['password'])

		data = dict()
		data['level'] = loglevel.upper()
		data['service'] = c.get('service')
		data['subject'] = subject

		mail_receivers = c['receivers']
		mail_from = '%s <%s>' % (c['sender'], c['user']) if 'sender' in c else c['user']		
		mail_subject = self.subject_format % data
		mail_body = body

		message = MIMEText(mail_body, 'plain')
		message['From'] = mail_from
		message['Subject'] = mail_subject

		pprint(message)

		result = self.conn.sendmail(mail_from, mail_receivers, message.as_string())

		if not self.config['keep_alive']:
			self.conn.quit()
			self.conn = None

		return True if len(result) == 0 else False 

	def set_subject_format(self, format):
		self.subject_format = format

	def debug(self, subject, body):
		return self._send_alert('debug', subject, body)

	def info(self, subject, body):
		return self._send_alert('info', subject, body)

	def warning(self, subject, body):
		return self._send_alert('warning', subject, body)

	def error(self, subject, body):
		return self._send_alert('info', subject, body)

	def critical(self, subject, body):
		return self._send_alert('error', subject, body)

	def panic(self, subject, body):
		return self._send_alert('panic', subject, body)

	def omfg(self, subject, body):
		return self._send_alert('omfg', 'We are all going to die!!!' + subject, body)