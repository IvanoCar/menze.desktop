import json
import datetime
import os

class Essentials:
    def __init__(self):
        self.session = {}

        now = datetime.datetime.now()
        date = '%s %s %s' % ( now.day, now.month, now.year )

        desktop = os.path.join(os.environ['HOMEPATH'], 'Desktop')
        desktop = os.path.join(desktop, 'MENIJI')

        self.pdf_location = os.path.join(desktop, date)
        self.make_storage_dir()

    def make_storage_dir(self):
        if not os.path.exists(self.pdf_location):
            os.makedirs(self.pdf_location)
    
    def clear_session(self):
        self.session = {}

