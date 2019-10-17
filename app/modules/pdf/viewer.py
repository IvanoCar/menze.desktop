import webview
from multiprocessing import Process


class PDFViewerProcess(Process):
    def __init__(self, path, name):
        Process.__init__(self)
        self.path = path
        self.name = name

    def run(self):
        webview.create_window(self.name, 'file:///' + self.path)
