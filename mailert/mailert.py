import smtplib

from pprint import pprint

MISSING_PARAMETER_INFO = 'Parameter %s is missing!'
WRONG_FORMAT_INFO = 'Connection string should look like: user:password@host[:port].'

OBLIGATORY_PARAMETERS = ['host', 'user', 'password', 'service', 'receivers']

class MailertException(Exception): pass
class RequiredParameterMissingException(MailertException): pass
class InvalidConnectionStringFormat(MailertException): pass

class Mailert(object):
	
	title_format = '[%(level)s] %(service)s - %(title)s'

	conn = None
	config = dict()

	def __init__(self, **kwargs):
		"""
		Mailert initialization. Available options:
		
		host
		port
		ssl
		timeout
		user
		password
		service
		sender
		receivers
		connstr

		"""

		args = kwargs.copy()

		# TODO: Handle logins with '@'
		if 'connstr' in args:
			connstr = args['connstr']
			if '@' in connstr:
				user_password, host_port = connstr.split('@')				
				if ':' in user_password:
					args['user'], args['password'] = user_password.split(':')
				else:
					raise InvalidConnectionStringFormat, WRONG_FORMAT_INFO
				if ':' in host_port:
					host, port = host_port.split(':')
				else:
					host = host_port
					port = None
				args['host'], args['port'] = host, port
			else:
				raise InvalidConnectionStringFormat, WRONG_FORMAT_INFO

		self.__check_if_parameters_are_missing(args)

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

		if 'sender' in args:
			self.config['sender'] = args['sender'] 

		return True

	def __check_if_parameters_are_missing(self, params):
		for key in OBLIGATORY_PARAMETERS:
			if key not in params:
				raise RequiredParameterMissingException(MISSING_PARAMETER_INFO % key)

	def debug(self, title, body):
		return self._send_alert('debug', title, body)

	def info(self, title, body):
		return self._send_alert('info', title, body)

	def warning(self, title, body):
		return self._send_alert('warning', title, body)

	def error(self, title, body):
		return self._send_alert('info', title, body)

	def critical(self, title, body):
		return self._send_alert('error', title, body)

	def panic(self, title, body):
		return self._send_alert('panic', title, body)

	def _send_alert(self, loglevel, title, body, **kwargs):
		c = self.config

		self.__check_if_parameters_are_missing(c)

		pprint(c)

		if not self.conn:
			constructor = smtplib.SMTP if c.get('ssl', None) is None else smtplib.SMTP_SSL
			self.conn = constructor(c.get('host', ''), c.get('port', None))
			self.conn.login(c.get('user', ''), c.get('password', ''))

		data = dict()
		data['level'] = loglevel.upper()
		data['service'] = c.get('service')
		data['title'] = title
		
		title = self.title_format % data
		body = body
		
		print title
		print body

		# TODO
		return True

