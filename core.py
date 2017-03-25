#!/usr/bin/python
import MySQLdb
import os
import sys
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
class Screenshot(QWebView):
    def __init__(self):
        self.app = QApplication(sys.argv)
        QWebView.__init__(self)
        self._loaded = False
        self.loadFinished.connect(self._loadFinished)

    def capture(self, url, output_file):
        self.load(QUrl(url))
        self.wait_load()
        # set to webpage size
        frame = self.page().mainFrame()
        self.page().setViewportSize(frame.contentsSize())
        # render image
        image = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        frame.render(painter)
        painter.end()
        print 'saving', output_file
        image.save(output_file)

    def wait_load(self, delay=0):
        # process app events until page loaded
        while not self._loaded:
            self.app.processEvents()
            time.sleep(delay)
        self._loaded = False

    def _loadFinished(self, result):
        self._loaded = True

db = MySQLdb.connect("localhost","root","1","coding" )
cursor = db.cursor()
sql = "SELECT * FROM TASKS WHERE status ='1'" 
cursor.execute(sql)
results = cursor.fetchall()
s = Screenshot()
for row in results:
   idee = row[1]
   urls = row[3]
   os.makedirs(idee)
   i = 0
#  here onwards main thing shuru
   websites = urls.split(';')
   for website in websites:
    	i = i + 1
   	filename = str(i) + '.png'
   	s.capture(website,os.path.join(idee,filename))
   	info = 'Readme.txt'
   	target = open(os.path.join(idee,info), 'a+')
   	target.write("%s --> %s"%(website,filename))
   	target.write("\n")
   sql = "UPDATE TASKS SET status='0' WHERE id= '%s'" % (idee)
   cursor.execute(sql)
   db.commit()


