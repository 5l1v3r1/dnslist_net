#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import sys
import os
from time import gmtime, strftime
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
		else:
			for host in hosts:
				hosts_retval.append(host.string)
		return hosts_retval

        
def timestamp():
        return strftime("%H:%M:%S", gmtime())

def hakz(r):
        for result in r:
                print("[+] {0}".format(result))

def banner():
        print("""\33[34m
      _             _ _     _   
   __| |_ __  ___  | (_)___| |_ 
  / _` | '_ \/ __| | | / __| __|
 | (_| | | | \__ \ | | \__ \ |_ 
  \__,_|_| |_|___/ |_|_|___/\__|
                    by \33[33m@zer0pwn\33[0m
 """)

#print(len(sys.argv))
if(len(sys.argv) == 3 and sys.argv[1] == "lookup"):
        arg0   = sys.argv[0]
        option = sys.argv[1]
        target = sys.argv[2]
        DNSLIST = dnslist_net()
        print("\n\33[32m[{0}] running lookup on {1}...\n".format(timestamp(), target))
        banner()
        result = DNSLIST.lookup(target)
        hakz(result)
        print("\n")
        
else:
        banner()
        print("\33[31musage:\33[0m {0} lookup google.com\n\n".format(sys.argv[0]))
