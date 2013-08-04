#!/usr/bin/env python                                                                                                                                                                            
# -*- coding: utf-8 -*-

import subprocess
import os
import sys

from tempfile import mkstemp
from shutil import move

TMP_FILE = "temp.java"

class Util(object):
    
    @staticmethod
    def clean_up(filenames):
        '''
        Removes any compiled files in the current directory.
        '''
        filelist = [ f for f in os.listdir(".") if (f.endswith(".class") or f.endswith(".pyc"))  ]
        for f in filelist:
            os.remove(f)
        
        for filename in filenames:
            Util.remove_file(filename)

    @staticmethod
    def remove_file(filename):
        if os.path.exists(filename):
            os.remove(filename)
    
    @staticmethod
    def compile_java(java_files):
        '''
        Compiles the java files given.  Throws an Exception when the Java cannot compile.
        '''
        for java_file in java_files:
            cmd = 'javac ' + java_file
            proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
            subprocess.Popen.wait(proc)

            full_exception = ""
            for line in proc.stderr.readlines():
                full_exception += line
                raise Exception("Could not compile changes: %s" % full_exception)
    
    @staticmethod
    def run_java(java_files):
        '''
        Executes the java files given.  Returns True if any output occurs.
        '''
        produces_output = False
        for java_file in java_files:
            class_array = java_file.split('.')
            cmd = 'java ' + class_array[0].capitalize()
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            subprocess.Popen.wait(proc)
            for line in proc.stdout.readlines():
                produces_output = True
                sys.stdout.write(line)

        return produces_output

    @staticmethod
    def pretty_class(java_file):
        '''Puts each statement onto a new line, to be used for saving output'''
        f = open(java_file)
        fh, abs_path = mkstemp()
        temp_file = open(abs_path, 'w')
        for line in Util.disassemble_class(f.read()):
            temp_file.write(line)
            temp_file.write("\n")

        f.close()
        temp_file.close()
        return abs_path

    @staticmethod
    def disassemble_class(class_text):
        '''
        Converts the class string into an array of lines 
        that make up the method.  Used simply to make the 
        Java file look prettier for saving.
        '''
        eol_chars = ['{', ';', ':', '}']
        lines = []
        last_eol = 0
        for i, c in enumerate(class_text):
            if c in eol_chars:
                lines.append(class_text[last_eol:i+1])
                last_eol = i + 1
        return lines