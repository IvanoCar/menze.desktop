import json
import os

from .exceptions import DatabaseError
from app.modules.utils import utility
from app import API_CLIENT

class Database:
    storage = None

    def __init__(self):
        self.storage = {}
        location = os.path.join(os.environ['HOMEPATH'], 'Documents')
        self.location = os.path.join(location, 'database.menze')

        try:
            self.read()
        except DatabaseError:
            pass

    def save(self):
        with open(self.location, 'w') as f:
            f.write(json.dumps(self.storage))

    def read(self):
        try:
            with open(self.location, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())
                self.storage = data
        except (FileNotFoundError, json.JSONDecodeError):
            if not utility.Utility.check_internet():
                raise DatabaseError                        
            users = API_CLIENT.get_users()         
            self.storage = {'users': users, 'food': {}}
            self.save()
            
