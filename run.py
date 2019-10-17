import webview
import time
import sys
from app import app
from threading import Thread
from multiprocessing import Process, freeze_support


def run():
    app.run(port=6247)
    

if __name__ == '__main__':
    freeze_support()

    t = Process(target=run)
    t.start()

    time.sleep(1)
    webview.create_window('Menze - aplikacija', 'http://127.0.0.1:6247/',  min_size=(1024, 600))
    t.terminate()
