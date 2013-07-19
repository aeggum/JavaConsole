#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

HEADER = "JavaConsole 0.8 - %s" % str(datetime.now().strftime("%b %d, %G"))

class Help(object):

	@staticmethod
	def print_help(help_arg):
		print HEADER
		if help_arg is not None:
			Help._print_help(help_arg)
			return 

		print "usage: ./console.py <options>"
		print "Java Console is meant to be used as a quick Java testing playground.  To use the console, simply write complete Java code.  The code will be compiled and executed. \
Methods can be added, provided the opening brace is given on the same line as the rest of the method declaration.  Classes will be supported in the future.  The following packages \
are imported by default: \n\tjava.util.*\n\tjava.lang.*\n\tjava.math.*\n\tjava.net.*\n\tjava.io.*\nIf more packages are required, they can be imported, assuming that they exist in \
your environment."
		print """
-h (--help) 	Print this help information.  Placing this before any other option will provide help specifically for that option.

-v (--verbose) 	Display more verbose messages, including the Exception message when one occurs.

-s (--save) 	Save the contents of the Java you've created on exit.
		The contents will be saved in the /tmp/javaconsole/<timestamp> directory, which will be created if it doesn't exist.  
		Alternatively, at any point during when working with the console, you may input '--save'.   This will save the current state.
"""

	@staticmethod
	def _print_help(option):
		if option == 'help':
			Help._print_help_help()
		elif option == 'save':
			Help._print_save_help()
		elif option == 'verbose':
			Help._print_verbose_help()

	@staticmethod
	def _print_help_help():
		print """
-h (--help) 	Print this help information.  Placing this at the end of any other option will provide help specifically for that option.
"""
	
	@staticmethod
	def _print_save_help():
		print """
-s (--save) 	Save the contents of the Java you've created on exit.
		The contents will be saved in the /tmp/javaconsole/<timestamp> directory, which will be created if it doesn't exist.

		Alternatively, at any point during when working with the console, you may input '--save'.   This will save the currently compiled state.
"""
	
	@staticmethod
	def _print_verbose_help():
		print """
-v (--verbose) 	Display more verbose messages, including the Exception message when one occurs.
"""