import requests
import json
from .exceptions import *

class Client:

    def __init__(self, base_url, keys):
        self.keypair = {
            'GET': keys['api-keys']['GET'],
            'EDIT-CREATE-DELETE': keys['api-keys']['EDIT-CREATE-DELETE']
        }
        self.client_id = keys['client_id']
        self.base_url = base_url
    
    def get_stats(self, restaurant_id):
        url = '%s/restaurants/%s/analytics' % (self.base_url, restaurant_id)
        h = { 'api-key': self.keypair['GET'], 'client_id': self.client_id, 'content-type': 'application/json' }
        r = requests.get(url, headers=h).text
        print(r)        
        stats = json.loads(r)
        return stats['results']
    
    def update_stats(self, restaurant_id):
        url = '%s/restaurants/%s/analytics' % (self.base_url, restaurant_id)
        h = { 'api-key': self.keypair['EDIT-CREATE-DELETE'], 'client_id': self.client_id, 'content-type': 'application/json' }
        
        data = {}
        try:
            r = requests.put(url, json=json.dumps(data), headers=h)
        except requests.exceptions.ConnectionError:
            raise UpdateFailed        
        if r.status_code != 200:
            raise UpdateFailed

    def update_food(self, restaurant_id, data):
        url = '%s/restaurants/%s/food' % (self.base_url, restaurant_id)
        h = { 'api-key': self.keypair['EDIT-CREATE-DELETE'], 'client_id': self.client_id, 'content-type': 'application/json' }
        
        data = { 'food_data': data }
        try:
            r = requests.put(url, json=json.dumps(data), headers=h)  
        except requests.exceptions.ConnectionError:
            raise UpdateFailed
        
        if r.status_code != 200:
            raise UpdateFailed

    # def get_food(self, restaurant_id): 
    #     url = '%s/restaurants/%s/food' % (self.base_url, restaurant_id)
    #     h = { 'api-key': self.keypair['GET'], 'client_id': self.client_id, 'content-type': 'application/json' }
    #     food = json.loads(requests.get(url, headers=h).text)

    #     return food['results']

    def get_users(self):
        url = self.base_url + '/users'
        h = { 'api-key': self.keypair['GET'], 'client_id': self.client_id , 'content-type': 'application/json'} # NO-CACHE? +        implementirati code-decode haširanog passworda
        users = json.loads(requests.get(url, headers=h).text)
        return users['results']

    def check_health(self):
        url = self._base_url + '/healthcheck'
        try:
            r = requests.get(url, headers=h).json
            if r['STATUS'] == 'running':
                return True
            return False        
        except (requests.exceptions.ConnectionError, json.JSONDecodeError, ValueError):
            return False
