#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import time
import os
from cmd import Cmd
class dnslist_net():
	"""
	this is just to please dnslist.net's formatting
	dnslist.domain_format("accounts.google.com")
	>>> returns /com/google/accounts
	"""
	def domain_format(self, target):
		retval = ''
		target_list = target.split('.')
		for x in reversed(target_list):
			retval += '/{0}'.format(x)
		return retval
	"""
	look up dns records
	"""
	def lookup(self, target):
		hosts_retval = []
		formatted_target = self.domain_format(target)
		# send the request
		r = requests.get("http://dnslist.net/{0}/".format(formatted_target))
		# parse the request
		doc = BeautifulSoup(r.text.strip(), "html.parser")
		title = doc.find('title')
		hosts = doc.find_all('a')
		arecords = doc.find_all('li')
		if(arecords):
			for record in arecords:
				hosts_retval.append(record.string)
		# if the list appears to be an index
		if("index for" in title.string):
			# get all tags in the index 
			# iterate through each index entry, retrieve data
			for a in hosts:
				if(a.string != "(idn)"):
					target = "{0}/{1}".format(formatted_target, a.string)
					r = requests.get("http://dnslist.net/{0}/".format(target))
					doc = BeautifulSoup(r.text.strip(), "html.parser")
					hosts = doc.find_all('a')
					# append every host entry to hosts_retval
					for host in hosts:
						hosts_retval.append(host.string)
		# if the list does not appear to be an index
		else:
			for host in hosts:
				hosts_retval.append(host.string)
		return hosts_retval
		# well i guess ill space this with a useless comment :)
		# hmu @zer0pwn on twitter for a chance to win absolutely nothing
class ui(Cmd):
	green = '\033[92m'
	bold = '\033[1m'
	end = '\033[0m'
	dns_list = dnslist_net()
	prompt = 'dnslist > '
	intro = """
	 _     __   ___ _____             _____
	| \|\|(_ |   | (_  |          |\||_  | 
	|_/| |__)|___|___) |    ___   | ||__ | 

	     	 a dns mapping aid

	{0}{1}usage: lookup linksys.com{2}

	domains with many recorded entries will take 
	a little bit longer than usual to process. do
	not fret, this is normal

	try using this tool recursively. for example,
	timhortons.ca points to www.timhortons.ca. a
	lookup of www.timhortons.ca returns its A records
	>>>
			[+]  a  165.160.13.20 
			[+]  a  165.160.15.20
	<<<

			""".format(bold, green, end)
	def do_lookup(self, target):
		print(self.bold+self.green+"started at {0}".format(time.asctime())+self.end)
		results = self.dns_list.lookup(target)
		for r in results:
			time.sleep(0.005)
			print("[+] {0}".format(r))
		print("\n")
	def do_help(self, void):
		print(self.intro)
	def do_EOF(self, void):
		return(True)
	def do_clear(self, void):
		os.system('clear')
	def do_cls(self, void):
		os.system('cls')
	def do_exit(self, void):
		return(True)


if __name__ == "__main__":
	ui = ui()
	ui.cmdloop()
