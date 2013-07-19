#!/usr/bin/env python                                                                                                                                                                            
# -*- coding: utf-8 -*-

import subprocess
import os
import sys

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