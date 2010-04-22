#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name: rc.conf syntax checker
# Description: Simple script which checks for syntax errors in the /etc/rc.conf file
# on the FreeBSD / NetBSD systems.
#
# Ideally you would use it in a combination with a vim mapping which would run this
# script and only save the file if it does not contain any syntax errors.
# Author: Tomaz Muraus (http://www.tomaz-muraus.info)
# Version: 1.0.0
# License: GPL

# Requirements:
# - Python >= 2.5

from __future__ import with_statement

import re
import sys
from optparse import OptionParser

def check_syntax(config_file = '/etc/rc.conf', print_report = True):
	""" Returns True if file does not contains syntax errors, False otherwise. . """

	valid_syntax = r'\w+(\s)*=(((\s)*("(\w|\s|/|\\|\-|\+|\.|\||\*|\?|,|=|:)*")|(\'(\w|\s|/|\\|\-|\+|\.|\||\*|\?|,|=|:)*\'))|\w+)(\s*#.*?)?$'
	
	line_num = 1
	errors = []
	try:
		with open(config_file, 'r') as file:
			line = file.readline()
			
			while line:
				skip = False
				error = False
	
				# Whitespace characters are allowed
				if re.match(r'^\s+$', line):
					skip = True
					
					
				# Check for hash character (possible comment)
				hash_position = line.find('#')
				
				if not skip and not error and hash_position != -1:
					# Only spaces or tabs can be located before the first hash
					invalid_chars = len([line[i] for i in range(0, hash_position)
							if line[i] != ' ' and line[i] != '\t'])
					
					if invalid_chars > 0 and not re.match(valid_syntax, line):
							error = True
					else:
						skip = True
						
				if not skip and not re.match(valid_syntax, line):
					error = True
					
				if error:
					errors.append((line_num, line.strip()))
					
				line_num += 1
				line = file.readline()
	except IOError:
		print >> sys.stderr, 'Fille %s cannot be opened.' % (config_file)
		return
	
	if errors:
		if print_report:
			errors = ['%s:%d %s' % (config_file, error[0], error[1]) for error in errors]
			print >> sys.stderr, 'The following syntax errors were detected in your config file:'
			print >> sys.stderr, '\n' . join(errors)
		
		return False
	
	if print_report:
		print 'File %s contains no syntax errors.' % (config_file)

	return True

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-f', '--file', dest = 'file', default = '/etc/rc.conf',
                  help = 'which config file to check for syntax errors',
                  metavar = 'FILE')
	
	(options, args) = parser.parse_args()
	
	check_syntax(options.file)