#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
PURPOSE:
Check that OAI-MPH services are responding. Also get some metadata info about
the service

AUTHOR:
    Magnar Martinsen, METNO/FOU, 2019-01-17 
      

UPDATED:
    Magnar Martinsen, METNO/FOU, 2019-01-17 
        Modified to Python

COMMENTS:
    - beta testing stage
"""

import sys
import os
import yaml
import logging
import logging.handlers
from argparse import ArgumentParser
import requests
from urlparse import urlparse

#Initiate logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")
LOG = logging.getLogger("CheckOAI-MPH")

class CheckOAISimple:

    #Initate class with logger
    def __init__(self, logfilename, log_level=logging.INFO):
        logging.FileHandler("{0}".format(logfilename))
        self.log = logging.getLogger("CheckOAI")
        self.log.setLevel(log_level)
        self.log.debug("Init class CheckOAI")

    # Read config file
    def readConfig(self, cfgfile):
        self.log.debug("Reading config file")
        try:
            self.cfg = yaml.safe_load(open(cfgfile))

        except Exception as e:
            self.log.error("Failed to open config: " + cfgfile + "\n",
                           exc_info=True)
        self.log.debug("Sucess reading config file")

    def checkProvider(self, url):
        """
        Check OAI-PMH provider. A valid Identity response, is considered
        is considered as provider online. An exception is considered provider offline 
        """
        response = False
        try:
            r = requests.get(url, params = {'verb' : 'Identify'}, timeout=5)
                    
            if(r.status_code == requests.codes.ok):
                response = True
            else:
                self.log.debug("Error: " + r.raise_for_status())
            r.close
        except Exception as e:
            self.log.info(e)
        return response
        
                 
    # Check servers listed in configfile
    def checkServers(self):
        for section in self.cfg:
            if self.cfg[section]['protocol'] == 'OAI-PMH':
                self.log.debug("Checking provider: " + section)
                self.log.debug("URI: " + self.cfg[section]['source'])
                #Check for valid response
                response = self.checkProvider(self.cfg[section]['source'])                 
                if(response):
                    self.log.info("Provider " + section + ": "
                             +  self.cfg[section]['source'] + " is ONLINE")
                if not(response):
                     self.log.info("WARINING!!! Provider " + section + ": "
                             +  self.cfg[section]['source'] + " is OFFLINE")
                     http_ok = self.check_http(self.cfg[section]['source'])
                     ping_ok = self.check_ping(self.cfg[section]['source'])
                     
                     
            #self.log.info("\n")


    # Ping hostname 
    def check_ping(self,url):
        hostname = urlparse(url).netloc
        self.log.info("Hostname to ping is: " + hostname)
        response = os.system("ping -c 1 " + hostname + ">/dev/null")
        # and then check the response...
        if response == 0:
            self.log.info("Ping OK")
            pingstatus = True
        else:
            self.log.info("Ping FAILED")
            pingstatus = False
        return pingstatus

    #Check for responsing webserver
    def check_http(self,url):
        parse_res = urlparse(url)
        url_parse = parse_res.scheme + "://" + str(parse_res.netloc) + "/"
        self.log.info("Check webserver with address: " + url_parse)
        http_status_ok = False
        try:
            r = requests.head(url_parse)
            self.log.info("check http returned status code : " + str(r.status_code))
            if(r.status_code == 200 or r.status_code == 301):
                http_status_ok = True
        except Exception as e:
            self.log.info("HTTP ERROR: " + str(e))
        
        return http_status_ok
    
def main():

    #Parse commandline arguments
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Increase output verbosity",
                        action="store_const", const=logging.DEBUG,
                        default=logging.INFO)
    parser.add_argument("-l", "--logfile", help="Specifiy logfile output.",
                        metavar="<logfilename>", default="out.log")
    parser.add_argument("-c", "--config", help="Specify mdharvest config file",
                        metavar="<filename>", required=True)
    

    #Get the Args
    args = parser.parse_args()
    LOG.debug("Logfile is: " + args.logfile)
    LOG.debug("Configfile is: " + args.config)

    #Init the class with logger
    check = CheckOAISimple(args.logfile,args.verbose)
    LOG.debug("Class initiated")

    #Read the configfile
    check.readConfig(args.config)

    #Check that all providers in configfile is online
    check.checkServers()
    
if __name__ == '__main__':
    main()
