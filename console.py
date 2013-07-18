#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import fnmatch
import sys
import os
import time
from tempfile import mkstemp
from shutil import move
from os import remove, close
from util import Util
from help import Help

CLASS_KEYWORDS = 'class'
ACCESS_MODIFIERS = ['public', 'private', 'protected']
START_FILE = 'start.java'
MAIN_FILE = 'main.java'
INVALID_CLASS_ERROR = "invalidClassDeclaration"

class Console(object):

    def __init__(self):
        self.main_input = []
        self.imports = []
        self.methods = []
        self.method_names = []  # currently serves no purpose
        self.classes = []
        self.class_names = []
        self.full_class_names = []

    def run(self):
        '''
        Executes the successfully compiled java program, and if the program has any
        output, it will remove the change to the main method so that the same output
        doesn't happen on any subsequent additions to the main method.
        '''
        if Util.run_java([MAIN_FILE]) == True:
            self.main_input.pop()
    
    def build(self, is_main=False, is_method=False, is_class=False):
        '''
        Copies the base java file, moves the changes into it and compiles it.
        If an Exception occurs, the change is rolled back.
        '''
        shutil.copyfile(START_FILE, MAIN_FILE)
        self.parse_file(MAIN_FILE)
        
        # Attempt to compile the new change
        try:
            Util.compile_java(self.full_class_names)
        except Exception as e:
            if verbose_output == True:
                print 'Exception: %s' % e
            else:
                print 'An Exception occurred compiling the program'

            # Determine who caused the exception and remove the code
            if is_main is True:
                self.main_input.pop()
            elif is_method is True:
                self.methods.pop()
                self.method_names.pop()
            elif is_class is True:
                self.classes.pop()
                self.class_names.pop()
                filename = self.full_class_names.pop()
                self._remove_file(filename)

            return

        if is_main is True:
            self.run()

    def console(self):
        '''
        The 'main' method for the Java Console application.
        '''
        shutil.copyfile(START_FILE, MAIN_FILE)
        self.full_class_names.append(MAIN_FILE)
        print "Java Console: run Java with no setup required."
        
        try: 
            while True:
                Util.clean_up(self.full_class_names)
                self.general_input()
        except KeyboardInterrupt:
            print ''
        except Exception as e:
            print e     # for debugging
        finally:
            Util.clean_up(self.full_class_names)
            if save_output == True:
                save_output(self)

            print 'Cya'
          

    def general_input(self):
        '''
        Basic input handler for the application.  Main method content is the expected common case,
        but will also handle special strings such as 'clear' and 'exit', as well as methods, import
        statements and in the future, classes.
        '''
        while True:
            user_input = raw_input("main> ")

            if user_input.find("clear") != -1:
                self.main_input = []
                continue
            
            if user_input.find("--save") != -1:
                self.save_output()
                continue

            if user_input.find('exit') != -1:
                raise Exception("exiting")

            if len(user_input) == 0: # a new line is given
                continue
                      
            if len(fnmatch.filter([user_input], "*class*")) == 1:
                self.handle_class(user_input)
            elif self.is_method_declaration(user_input) == True:
                self.handle_method(user_input)
            elif len(fnmatch.filter([user_input], "import*")) == 1:
                self.imports.append(user_input)
            else: 
                self.main_input.append(user_input)
                self.build(is_main=True)
    

    def handle_method(self, method_declaration):
        """
        Adds a method to the Console program.  Must have opening brace
        on the same line as declaration.
        """
        unclosed = True
        user_input = method_declaration
        self.extract_method_name(method_declaration)
        while unclosed == True:
            new_input = raw_input("..... ")
            user_input += new_input
            if new_input.find("}") != -1:
                unclosed = False
        
        self.methods.append(user_input)
        self.build(is_method=True)


    def handle_class(self, class_declaration):
        openers = 1
        user_input = class_declaration
        try:
            self.extract_class_name(class_declaration)
            while openers > 0:
                new_input = raw_input("..... ")
                user_input += new_input
                if new_input.find("{") != -1:
                    openers += 1
                if new_input.find("}") != -1:
                    openers -= 1
            self.classes.append(user_input)
            self.create_class()
            self.build(is_class=True)
        
        except Exception as e:
            if str(e) == INVALID_CLASS_ERROR:
                print "extending or implementing other classes or interfaces is not supported"
        
       
    def parse_file(self, java_file):
        '''
        Parses the initial java file, and adds the import statements, main 
        method content, and individual methods.  Just basic search/replace.
        '''
        f = open(java_file)
        fh, abs_path = mkstemp()
        new_file = open(abs_path, 'w')
        for line in f.readlines():

            # Insert main input
            if line.find("____") != -1:
                new_file.write(line.replace("____", "\n\t\t".join(self.main_input)))
            
            # Insert methods
            elif line.find("----") != -1:
                method_section = ""
                for method in self.methods:

                    method_lines = self.disassemble_method(method)
                    for index, value in enumerate(method_lines): 
                        method_section += method_lines[index]
                        method_section += "\n\t"

                    method_section += "\n\t"

                new_file.write(line.replace("----", method_section))

            # Insert import statements
            elif line.find("****") != -1:
                new_file.write(line.replace("****", "\n".join(self.imports)))
            else:
                new_file.write(line)
                
        
        new_file.close()
        close(fh)
        f.close()
        remove(java_file)
        move(abs_path, java_file)

    def disassemble_method(self, method):
        '''
        Converts the method string into an array of lines 
        that make up the method.  Used simply to make the 
        Java file look prettier for saving.
        '''
        eol_chars = ['{', ';', ':', '}']
        lines = []
        last_eol = 0
        for i, c in enumerate(method):
            if c in eol_chars:
                lines.append(method[last_eol:i+1])
                last_eol = i + 1
        return lines

    def is_method_declaration(self, user_input):
        '''
        Returns true if the user input is a declaration of a method.
        '''
        for modifier in ACCESS_MODIFIERS:
            if modifier in user_input and user_input.endswith("{"):
                return True

        return False

    def extract_method_name(self, method_declaration):
        '''
        Determines the name of the method being created.
        '''
        for m in method_declaration.split(" "):
            if m.find("(") != -1:
                self.method_names.append(m[:m.find("(")])

    def extract_class_name(self, class_declaration):
        if class_declaration.find("implements") != -1 or \
                    class_declaration.find("extends") != -1:
            raise Exception(INVALID_CLASS_ERROR)
        class_name = class_declaration.split(" ")[-2]
        
        # If the class was previously added, remove all references to it
        if self.class_names.count(class_name) != 0:
            index = self.class_names.index(class_name)
            del self.class_names[index]
            del self.classes[index]
            del self.full_class_names[index]
        
        self.class_names.append(class_name)
        
    def create_class(self):
        '''
        Create a new file using the class name, and then copy the class
        contents into the new file.
        '''
        filename = "%s.%s" % (self.class_names[-1], 'java')
        self._remove_file(filename)
        
        self.full_class_names.append(filename)
        file = open(filename, 'w+')
        for line in self.classes:
            file.write(line)
        file.close()
        

    def save_output(self):
        directory = '/tmp/javaconsole/%s' % int(time.time())
        if not os.path.exists(directory):
            os.makedirs(directory)
            shutil.copyfile(MAIN_FILE, directory + '/main.java')
            
    def _remove_file(self, filename):
        if os.path.exists(filename):
            os.remove(filename)


print_help = False
verbose_output = False
save_output = False

for arg in sys.argv:
    if '-h' == arg or '--help' == arg:
        print_help = True
    if '-v' == arg or '--verbose' == arg:
        verbose_output = True
    if '-s' == arg or '--save' == arg:
        save_output = True


if print_help == True:
    Help.print_help()
else:
    # Execute the Console program
    console = Console()
    console.console()