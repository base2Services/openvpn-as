#!/usr/bin/python3
# Uses env var AWSREGIONS to
# extract selected aws ip's into ovpn format
# at designated file location
# Hacked together by Lewis Shobbrook 2018
# Updated Jan 2020

import os, subprocess, test, sys, re, json, urllib.request, datetime, pprint
from subprocess import call
from urllib.request import urlopen

#Defaults
retstr=""
response = urlopen("https://ip-ranges.amazonaws.com/ip-ranges.json")
jsdata = str((response.read().decode('utf-8')))
datafile = (os.getenv('DATAFILE', default='/data/ip-ranges.json'))
awsregions = (os.getenv('AWSREGIONS', default='ap-southeast-2'))
olddata = open(datafile,'a+')
filesize = os.path.getsize(datafile)
#print(filesize)

def awsips(awsregions,filesize):
    newips = []
    oldips = []
    ips = json.loads(jsdata)
    if filesize > 1: # Only read old json if it exists
        olddata = open(datafile).read()
        oldip = json.loads(olddata)
        for ip in oldip['prefixes']:
            if re.search(ip['region'], awsregions):
                oldips.append(str(ip['ip_prefix']))
    #print(oldips)            
    for ip in ips['prefixes']:
        if re.search(ip['region'], awsregions):
            newips.append(str(ip['ip_prefix']))
    ipdiff = tuple(set(newips) - set(oldips))
    for ip in ipdiff:
        subprocess.call("/usr/bin/docker exec openvpn-as bash -c '/config/scripts/sacli --user aws --key vpn.server.routing.private_network.111111 --value \""+ str(ip) + "\" ConfigPut\n'", shell=True)
    return ipdiff

queryip = awsips(awsregions,filesize)
olddatahandle = open(datafile,"w+")
olddatahandle.write(jsdata)
olddatahandle.close
cmd = "/usr/bin/docker exec openvpn-as bash -c 'cd /config/scripts && ./sacli start'"
if queryip:
    returned_output = subprocess.run(cmd, shell=True)
#print(returned_output)
