"""
A collection of handy functions for making python microservices work in the real world
"""

from os import getpid, getenv
from socket import getfqdn,  gethostbyname
#import logging
import urllib2
import json


def send_request_to_bus(input_dict,host,port,topic):
    """ this is intended for publishing via http to a messaging bus """
    encoded_args = json.dumps(input_dict)
    url = 'http://' + host + ':' + port + '/put?topic=' + topic
    urllib2.urlopen(url, encoded_args).read()
    return True    


def describe_service():
    """ this gets the essential datapoints required for monitoring a python script running as a service"""
    service_description = {}
    service_description['hostname'] = getfqdn()
    service_description['ip_address'] = gethostbyname(getfqdn())
    service_description['process_id'] = getpid()
    service_description['script_name'] = __file__
    service_description['description'] = __doc__ # this takes the docstring from the top of the file, so fill it in!
#    send_request_to_bus(service_description,'service_registry')
    return service_description
    
