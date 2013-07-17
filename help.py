#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Help(object):

	@staticmethod
	def print_help():
		print "usage: ./console.py <options>"
		print "Java Console is meant to be used as a quick Java testing playground.  To use the console, simply write complete Java code.  The code will be compiled and executed. \
Methods can be added, provided the opening brace is given on the same line as the rest of the method declaration.  Classes will be supported in the future.  The following packages \
are imported by default: \n\tjava.util.*\n\tjava.lang.*\n\tjava.math.*\n\tjava.net.*\n\tjava.io.*\nIf more packages are required, they can be imported, assuming that they exist in \
your environment."
		print """
-h (--help) 	Print this help information.

-v (--verbose) 	Display more verbose messages, including the Exception message when one occurs.

-s (--save) 	Save the contents of the Java you've created on exit.
		The contents will be saved in the /tmp/javaconsole/ directory, which will be created if it doesn't exist.  
		To prevent overwriting the file repeatedly, the console contents are further separted by timestamp.  Use 'ls -lthr' to sort.
		Alternatively, at any point during when working with the console, you may input '--save'.   This will save the current state.
"""