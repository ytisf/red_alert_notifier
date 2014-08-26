#!/usr/bin/env python

import sys
import gtk
import appindicator
try:
	import easygui
except:
	print "Do 'sudo apt-get install python-easygui python-tk'"
	sys.exit(1)
import pygtk
pygtk.require('2.0')
import pynotify
import urllib2
from BeautifulSoup import BeautifulSoup


PING_FREQUENCY = 10     # seconds
URL_RED = "http://www.tzevaadom.com/history.html"
name = "Red Alert Notifier"


class CheckGMail:
	def __init__(self):
		self.ind = appindicator.Indicator("new-gmail-indicator", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
		self.ind.set_status(appindicator.STATUS_ACTIVE)
		self.ind.set_attention_icon("new-messages-red")
		self._last_alert = []
		self._firstrun = 1

		self.menu_setup()
		self.ind.set_menu(self.menu)

	def menu_setup(self):
		self.menu = gtk.Menu()

		self.about_item = gtk.MenuItem("About")
		self.about_item.connect("activate", self.about)
		self.about_item.show()
		self.menu.append(self.about_item)

		self.quit_item = gtk.MenuItem("Quit")
		self.quit_item.connect("activate", self.quit)
		self.quit_item.show()
		self.menu.append(self.quit_item)


	def main(self):
		print "[+] Initializing..."
		gtk.timeout_add(PING_FREQUENCY * 1000, self.check_alerts)
		gtk.main()

	def get_html(self):
		response = urllib2.urlopen(URL_RED)
		response = response.read()
		return response

	def get_table(self, html):
		alert = []
		all_alerts = []
		soup = BeautifulSoup(''.join(html))
		table = soup.find('table')
		rows = table.findAll('tr')
		for tr in rows:
			cols = tr.findAll('td')
		for td in cols:
			text = ''.join(td.find(text=True))
			alert.append(text)
		all_alerts.append(alert)
		alert = []
		return all_alerts

	def pop_alert(self, alert):
		pynotify.init("Basic")
		n = pynotify.Notification(alert[2], alert[3] + " - " + alert[1])
		n.set_timeout(pynotify.EXPIRES_DEFAULT)
		n.show()

	def about(self, widget):
		about_text = "Red Alert Notificator" \
		             "\n\nA notificator for GNOME and UNITY for red alerts.\n" \
		             "Please take this application as experimental and don't\n" \
		             "treat it as a working or final product. \n\n" \
		             "Please get updates from: https://ytisf.github.io/RedAlertNotifier/\n" \
		             "built by Yuval tisf Nativ and Bar Hofesh."
		easygui.msgbox(about_text, title=name)

	def quit(self, widget):
		sys.exit(0)

	def check_alerts(self):
		html_body = self.get_html()
		array_of_alerts = self.get_table(html_body)
		self._last_alert = array_of_alerts[0]

		if self._firstrun == 1:
			self.pop_alert(self._last_alert)
			self._firstrun = 0
			print "[+] Finished initialization."
			return 0, 0
		else:
			if array_of_alerts[0][2] == self._last_alert[2]:
				# Already saw this
				self.ind.set_status(appindicator.STATUS_ACTIVE)
				return 0, 0
			else:
				# New alert
				self.ind.set_status(appindicator.STATUS_ATTENTION)
				self.pop_alert(array_of_alerts[0])
				self._last_alert = array_of_alerts[0]
				return 1, 0


if __name__ == "__main__":
	indicator = CheckGMail()
	indicator.main()
