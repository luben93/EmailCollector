#!python

__author__ = "Lucas Persson"
__copyright__ = "Copyright 2015"
__credits__ = "Lucas Persson"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Lucas Persson"
__email__ = "luben93@gmail.com"

import urllib2
import re
from optparse import OptionParser
import time
from datetime import date, timedelta
import sys

import boto3 	# pip install boto3 
				# configure aws cli



regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

def get_emails(s):
    """Returns an iterator of matched emails found in string s."""
    # Removing lines that start with '//' because the regular expression
    # mistakenly matches patterns like 'http://foo@bar.com' as '//foo@bar.com'.
    return (email[0] for email in re.findall(regex, s) if not email[0].startswith('//'))

#def find_emails(str):
#	emails = re.findall(r'[\w\.-]+@[\w\.-]+', str) 
#	for email in emails:
#    	print email


def read_url(url,f):
	website = urllib2.urlopen(url)

    #read html code
	html = website.read()

 	yesterday = date.today() - timedelta(1)
 	todays=html[:html.find(yesterday.strftime("Posted:%a, %d %b %Y"))]



    #use re.findall to get all the links
	links = re.findall('"((http|ftp)s?://.*?)"', todays)
	for link in links:
		if "pastebin" in link[0]:
			try:
				website = urllib2.urlopen(link[0])
			except urllib2.HTTPError, e:
				print "Error"
				print link
				print e
			else:
				
				mail = website.read()
				for email in get_emails(mail): 
					f.write(email+'\n')


if __name__ == '__main__':


	filename=time.strftime("Mail-%d-%m-%Y.csv")
	url="https://haveibeenpwned.com/Pastes/Latest"
	bucket=sys.argv[1]#input 

	with open(filename, 'w') as f:
		read_url(url,f)
	f.closed

	data = open(filename, 'rb')
	s3 = boto3.resource('s3')
	print s3.Bucket(bucket).put_object(Key=filename, Body=data)
	
