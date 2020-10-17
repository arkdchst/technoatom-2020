import requests

import string
import random

class FailedLoginError(Exception):
	pass

class ResponseStatusCodeError(Exception):
	pass

def random_name(length=20):
	letters = string.ascii_letters
	return ''.join(random.choices(letters, k=length))


class Client:
	def __init__(self):
		self.session = requests.Session()

	def _request(self, method, url, accept_codes=None, data=None, headers=None, params=None):
		if accept_codes == None:
			accept_codes = range(200, 300)

		res = self.session.request(method, url, data=data, headers=headers, params=params)

		if not res.status_code in accept_codes:
			raise ResponseStatusCodeError(f'Response status code {res.status_code} not in {accept_codes}')

		return res


	def segment_exists(self, id_):
		res = self._request('GET', 'https://target.my.com/api/v2/remarketing/segments.json?limit=500')
		return id_ in [x['id'] for x in res.json()['items']]

	def auth(self, login, password):
		res = self._request('POST', 'https://auth-ac.my.com/auth',
			headers={
				'Referer' : 'https://target.my.com/',
			},

			data={
				'email' : login,
				'password' : password,
				'continue' : 'https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
			},
		)
		if 'Invalid login or password' in res.text:
			raise FailedLoginError('Invalid login or password')

		self.set_csrf()

	def set_csrf(self):
		self.csrf = self._request('GET', 'https://target.my.com/csrf/').cookies['csrftoken']

	def add_segment(self):
		name = random_name()
		res = self._request('POST', 'https://target.my.com/api/v2/remarketing/segments.json',
			data = '{"name":"'+ name +'","pass_condition":1,"relations":[{"object_type":"remarketing_player","params":{"type":"positive","left":365,"right":0}}],"logicType":"or"}',
			headers={'X-CSRFToken': self.csrf})

		return res.json()['id']

	def delete_segment(self, id_):
		self._request('DELETE', 'https://target.my.com/api/v2/remarketing/segments/'+ str(id_) +'.json',
			headers={'X-CSRFToken': self.csrf})
