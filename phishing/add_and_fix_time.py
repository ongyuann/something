#!/usr/bin/env python3

import csv
import re
import subprocess

#filename = "[SPPL] 2_11_2020 Delivery Fail  - Results.csv"

def get_csv_files():
    names = []
    output = subprocess.check_output(['ls'],encoding="UTF-8").split('\n')
    for name in output:
        #print (name[-4:])
        if name[-4:] == ".csv":
            names.append(name)
    #print (names)
    return names

def get_dates(columnname,filename):
    dates = []
    with open(filename,newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dates.append(row[columnname])
    print ("[+] retrieved " + str(len(dates)) + " '" + columnname + "' from " + filename)
    #print (senddates)
    return dates

#senddates_list = ["2020-11-02T05:28:23.095604467Z"]
def process_dates(dates_list):
    processed = []
    date_pattern = re.compile(r'\d\d\d\d-\d\d-\d\d')
    time_pattern = re.compile(r'\d\d:\d\d:\d\d')
    hours_to_add = 8 #CHANGETHIS
    for thisdate in dates_list:
        date = date_pattern.search(thisdate)
        time = time_pattern.search(thisdate)
        #print (date.group())
        #print (time.group())
        processed.append(add_hours(date.group(),time.group(),hours_to_add))
    #print (processed)
    #print ("[*] " + str(hours_to_add) + " hours added to all values")
    return processed

def add_day(date_string):
    day_value = int(date_string[-2:])
    next_day_value = day_value + 1
    if next_day_value < 10:
        next_day_value = '0' + str(next_day_value)
    next_day_string = date_string[:-2] + str(next_day_value)
    return next_day_string

def add_hours(date_string,time_string,hours_to_add):
    result = ''
    hours = int(time_string[0:2])
    new_hours = hours + hours_to_add
    if new_hours > 23:
        new_hours = abs(24 - new_hours)
        date_string = add_day(date_string)
    if int(new_hours) < 10:
        new_hours = '0' + str(new_hours)
    result += "Date: " + date_string
    result += " Time: " + str(new_hours) + time_string[2:]
    return result

#if __name__ == "__main__":
def main(columnname):
    for filename in get_csv_files():
        new_dates = process_dates(get_dates(columnname,filename))
        results_filename = "newdates_" + columnname + "_" + filename + ".txt"
        with open(results_filename,'w') as f:
            f.write('new ' + columnname + '\n')
            for newdate in new_dates:
                f.write(newdate)
                f.write("\n")
            f.close()
        print ("[+] new " + columnname + " results stored in " + results_filename + ".txt")
    pass

if __name__ == "__main__":
    main('send_date')
    main('modified_date')
