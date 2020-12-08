import requests

import config

def set(username, id):
	return requests.post(f'{config.VKAPI_URL}/service/set',json={'username':username,'id':id})

def unset(username):
	return requests.get(f'{config.VKAPI_URL}/service/unset/{username}')

def get_id(username):
	return requests.get(f'{config.VKAPI_URL}/vk_id/{username}').json()['vk_id']
