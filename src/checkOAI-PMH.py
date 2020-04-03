#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
PURPOSE:
Check that OAI-MPH services are responding. Also get some metadata info about
the service.
The sctript uses the same yaml-config file used for mdharvest tool. This tool
can be used to check for ONLINE availbility of providers in config before
harvesting.


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
from oaipmh.client import Client

#Initiate logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")
LOG = logging.getLogger("CheckOAI-MPH")

class CheckOAI:

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

         try:
            client = Client(url)
            ident = client.identify()
            self.log.debug("Service at: " + url + " is responding")
            self.log.debug("RepositoryName is: " + ident.repositoryName())
            self.log.debug("BaseURL is: " + ident.baseURL())
            return True

         except Exception as e:
            self.log.error("Problem with server at: " + url + "\n")
                         #,exc_info=True)
            return False
        
                 
    # Check servers listed in configfile
    def checkServers(self):
        for section in self.cfg:
            if self.cfg[section]['protocol'] == 'OAI-PMH':
                self.log.debug("\nChecking provider: " + section)
                self.log.debug("URI: " + self.cfg[section]['source'])
                response = self.checkProvider(self.cfg[section]['source'])                 
                if(response):
                    self.log.info("Provider " + section + ": "
                             +  self.cfg[section]['source'] + " is ONLINE")
                if not(response):
                     self.log.warn("Provider " + section + ": "
                             +  self.cfg[section]['source'] + " is OFFLINE")

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
    check = CheckOAI(args.logfile,args.verbose)
    LOG.debug("Class initiated")

    #Read the configfile
    check.readConfig(args.config)

    #Check that all providers in configfile is online
    check.checkServers()
    
if __name__ == '__main__':
    main()
