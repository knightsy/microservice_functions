"""
A collection of handy functions for making python microservices work in the real world
"""

from os import getpid, getenv
from socket import getfqdn,  gethostbyname
import logging
import urllib2
import json
import datetime
import traceback as tb


def send_request_to_bus(input_dict,host,port,topic):
    """ this is intended for publishing via http to a messaging bus """
    encoded_args = json.dumps(input_dict)
    url = 'http://' + host + ':' + port + '/put?topic=' + topic
    print url
    urllib2.urlopen(url, encoded_args).read()
    return True    


def describe_service(service_name='__file__ would be good here'):
    """ this gets the essential datapoints required for monitoring a python script running as a service"""
    service_description = {}
    service_description['hostname'] = getfqdn()
    service_description['ip_address'] = gethostbyname(getfqdn())
    service_description['process_id'] = getpid()
    service_description['service_name'] = service_name

    return service_description

    
class MessagingBusHandler(logging.Handler):
    """
    A class which sends records to a Web server, using either GET or
    POST semantics.
    """
    def __init__(self, host, port, topic, method="PUT"):
        """
        Initialize the instance with the host, the request URL, and the method
        ("GET" or "POST")
        """
        logging.Handler.__init__(self)
        method = method.upper()
        if method not in ["PUT"]:
            raise ValueError("method must be PUT")
        self.host = host
        self.port = port
        self.topic = topic
        self.method = method

            
    def emit(self, record, additionals_dict = {}):
        
        try:
            output_dict = record.__dict__
            
            if 'exc_info' in output_dict:
                if output_dict['exc_info']:
                    formatted = tb.format_exception(*output_dict['exc_info'])
                    output_dict['exception'] = formatted
                output_dict.pop('exc_info')

            output_dict["publication_type"] = 'APPLOG'
            output_dict['datetime'] = str(datetime.datetime.utcfromtimestamp(output_dict["created"]))
            for key, value in additionals_dict.iteritems():
                output_dict[key] = value

            encoded_args = json.dumps(output_dict)

            topic = self.topic
            host = self.host
            port = self.port
            
            url = 'http://'+ host + ':' + str(port) + '/put?topic=' + topic
            urllib2.urlopen(url, encoded_args).read()
            return True             
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)  
