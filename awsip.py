#!/usr/bin/python3
# Uses env var AWSREGIONS to
# extract selected aws ip's into ovpn format
# at designated file location
# Hacked together by Lewis Shobbrook 2018

import os, test, sys, re, json, urllib.request, datetime, pprint
from subprocess import call
from netaddr import *
from urllib.request import urlopen

#fileloc = "/etc/openvpn/ccd/DEFAULT"
fileloc = "./DEFAULT"

awsregions = (os.getenv('AWSREGIONS', default='ap-southeast-2'))
# aws ips
def awsips(awsregions):
    retstr=""
    response = urlopen("https://ip-ranges.amazonaws.com/ip-ranges.json")
    jsdata = str((response.read().decode('utf-8')))
    ips = json.loads(jsdata)
    aws = []
    for ip in ips['prefixes']:
        if re.search(ip['region'], awsregions):
            ipa = str(IPNetwork(ip['ip_prefix']).ip)
            mask = str(IPNetwork(ip['ip_prefix']).netmask)+"\""
            retstr+="push \"route "+ ipa + " " + mask + "\n"
    return retstr

retstr = awsips(awsregions)
if retstr != open(fileloc).read():
    filehandle = open(fileloc,"w")
    filehandle.write(retstr)
    filehandle.close
