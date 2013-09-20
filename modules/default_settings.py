# coding:utf-8
#settings.py includes configs for agent server

#import os


import interfaces
import logging

dataStore=interfaces.DataStore()

#SSL_CA_FILE="/etc/ssl/certs/ca-certificates.crt"
SECRET_SALT="djefioafeaz89gerajl"

#logging.basicConfig(filename="test.log",level=logging.DEBUG)
logger=logging.getLogger()
logger.addHandler(logging.FileHandler("test.log"))
logger.setLevel(logging.DEBUG)


#Packages
import packages
import packages.basics


