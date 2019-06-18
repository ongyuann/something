#!/usr/bin/python3

import re,os

#filename = "test.html"
#print("Enter filename of HTML ")
filename = input("Enter filename of HTML: ")
filename = filename.strip()
output = filename+'_output.txt'

try:
    output_file = open(output,'r')
    os.system('mv '+output+' '+output+'.old')
    output_file.close()
except:
    os.system('touch '+output)


with open(filename,'r') as document:
        line = document.readline()
        while line != "":
            if re.search(r'\b[A-Z]{8}\b',line):
                line = line.strip()
                line = line[4:12]
                os.system('echo '+line+' >> '+output)
                #print (line)
            line = document.readline()
        pass
print ('it is done. check '+output)
