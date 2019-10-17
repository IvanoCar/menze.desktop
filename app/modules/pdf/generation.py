import os
import time
import json
from xhtml2pdf import pisa


class PDF:
    def __init__(self, html):
        self.path = None
        self.html = html

    def save(self, path, name, date_time):
        n = '%s %s.pdf' % (name, date_time)
        p = os.path.abspath(os.path.join(path, n))
        self.path = p
        self.convert_and_save()

    def convert_and_save(self):
        result_file = open(self.path, "w+b")
        pisa_status = pisa.CreatePDF(
            self.html,
            dest=result_file)
        result_file.close()
