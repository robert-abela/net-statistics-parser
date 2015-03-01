#The MIT License (MIT)
#
#Copyright (c) 2015 Robert Abela
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
#See: https://github.com/robert-abela/net-statistics-parser

import os
import re
import csv

NP = r'(\d*)'   #number pattern

class Value:
    '''Internal class used to facilitate the ValueList management.'''
    def __init__(self, header, pattern, section, subsection = None):
        '''Contructor to create a new value that still needs to be parsed.'''
        self.header = header
        self.pattern = pattern
        self.section = section
        self.subsection = subsection

    def read_value(self):
        '''Calls ``netstat -es`` and parses the output to find the desired 
        value.'''
        self.value = self.__parse_value()

    def __parse_value(self):
        current_section = ''
        current_subsection = ''
        return_value = None
     
        #file = open(r'netstat.txt')
        #for line in file:
        for line in os.popen('netstat -es'):
            line = line.strip('\r\n')
            #print(line)
            if len(line) == 0: #skip empty line
                continue
            if line.endswith(':'): #section/subsection heading
                if line[0].isspace():
                    current_subsection = line.strip()
                else:
                    current_section = line.strip()
                    current_subsection = ''
                continue
            
            if (self.section == current_section):
                if not self.subsection or (self.subsection == current_subsection):
                    match = re.findall(self.pattern, line)
                    if match:
                        return_value = match[0]
                        break
        
        #file.close()
        return return_value
        
class ValueList:
    def __init__(self):
        '''Contructor for the ValueList class.'''
        self.values = []
    
    def write_csv(self, path):
        '''
        ``netstat -es`` command is called and the parsing takes place. At the 
        end this function writes the values extracted to a CSV file in the path 
        supplied. This file is always written over.
        
        Return: None
        '''
        headers_row = []
        values_row = []
        
        for value in self.values:
            value.read_value()
            headers_row.append(value.header)
            values_row.append(value.value)
            
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers_row)
            writer.writerow(values_row)
    
    
    def add_value_to_parse(self, header, pattern, section, subsection = None):
        '''
        Adds a new value that needs to be read from the netstat output.
        
        Parameter description: header will be used as the CSV heading for this 
        value. pattern will be used to match the line and extract a part of it. 
        section is the heading in netstat output where the value appears and 
        (optional) subsection is to be used only when applicable.
        
        Return: None
        '''
        self.values.append(Value(header, pattern, section, subsection))

###############################################################################
# Edit only below this comment
###############################################################################

my_list = ValueList()

my_list.add_value_to_parse('BSR', NP + ' bad segments received.','Tcp:')
my_list.add_value_to_parse('OO', 'OutOctets: ' + NP, 'IpExt:')
my_list.add_value_to_parse('DU', 'destination unreachable: ' + NP, 'Icmp:', 'ICMP input histogram:')

# Once ready adding values to be parsed, do the parsing and output to csv 
# (it will be over written every time).
my_list.write_csv(r'output.csv')
