#!/usr/bin/env python3

import csv
import re
import subprocess
from ipwhois import IPWhois

#filename = "[SPPL] 2_11_2020 Delivery Fail  - Results.csv" #change this

def get_csv_files():
    names = []
    output = subprocess.check_output(['ls'],encoding="UTF-8").split('\n')
    for name in output:
        #print (name[-4:])
        if name[-4:] == ".csv":
            names.append(name)
    #print (names)
    return names

#get_csv_files()

def get_ip(filename):
    ips = []
    with open(filename,newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ips.append(row['ip'])
    print ("[+] retrieved " + str(len(ips)) + " ip addresses from " + filename)
    #print (ips)
    return ips

#get_ip(filename)

def do_whois(list_of_ips):
    print ("[+] performing whois on all " + str(len(list_of_ips)) + " ip addresses ...")
    results = []
    for ip in list_of_ips:
        if ip == "":
            results.append("<no result>")
            continue
        try:
            obj = IPWhois(ip)
            info = obj.lookup_whois()
            owner = info["nets"][0]["description"]
            owner = owner.strip()
            owner = owner.replace('\n',' ').replace('\r',' ')
            print (owner)
            results.append(owner)
        except:
            results.append("<no result>")
            continue
    #print (results)
    return results


#do_whois(get_ip(filename))
def main():
    for filename in get_csv_files():
        whois_results = do_whois(get_ip(filename))
        results_filename = "whois_" + filename + ".txt"
        with open(results_filename,'w') as f:
            f.write('whois results\n')
            for result in whois_results:
                f.write(result)
                f.write("\n")
            f.close()
        '''
        with open("whois_results.csv","w") as csv_f:
            csv_f.write('whois results\n')
            for result in whois_results:
                csv_f.write(result)
                csv_f.write('\n')
            csv_f.close()
        '''
    print ("[+] whois results stored in " + results_filename)

if __name__ == "__main__":
    main()
