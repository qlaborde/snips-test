#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# @Author: laborde
# @Date:   2019-01-30T08:19:31+01:00
# @Email:  qlaborde@evertygo.com
# @Last modified by:   laborde
# @Last modified time: 2019-01-31T11:10:32+01:00

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import requests
# import sys


CONFIG_INI = "config.ini"


print 'truc'

class ImperiHome(object):

    def __init__(self):
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            self.config = None
            # sys.exit(1)

        # start listening to MQTT
        self.start_blocking()

    ############### Sub callback functions ###############

    # Get app code version
    def about_callback(self, hermes, intent_message):
        hermes.publish_end_session(intent_message.session_id, "")
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        print('self.config = ' + str(self.config))

        ip = self.config.get('secret').get('ip')
        port = self.config.get('secret').get('port')

        print('ip = ' + str(ip))
        print('port = ' + str(port))

        url = "http://"+ip+":"+port+"/api/rest/imperihome/about"
        print('url = ' + url)
        data = requests.get(url).json();
        hermes.publish_start_session_notification(intent_message.site_id, "I am a "+ str(data.get("device")) +". My version name is "+ str(data.get("versionName")) +" and my version code is " + str(data.get("versionCode")), "")

    # Get app code version
    def temp_callback(self, hermes, intent_message):
        hermes.publish_end_session(intent_message.session_id, "")
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        print('intent_message slots = ' + str(intent_message.slots))

        device_name = ""

        if len(intent_message.slots.device_name) > 0:
            device_name = intentMessage.slots.device_name.first().value
        else:
            device_name = 	"unknown"

        print("device_name = " + str(device_name))

        ip = self.config.get('secret').get('ip')
        port = self.config.get('secret').get('port')

        url = "http://"+ip+":"+port+"/api/rest/imperihome/about"
        print('url = ' + url)
        data = requests.get(url).json();
        hermes.publish_start_session_notification(intent_message.site_id, "The temperature of heater is " + str(data.get("versionCode")), "")

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'evertygo:about':
            self.about_callback(hermes, intent_message)
        if coming_intent == 'evertygo:temp':
            self.temp_callback(hermes, intent_message)

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes("localhost:1883") as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    ImperiHome()
