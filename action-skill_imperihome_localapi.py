# @Author: laborde
# @Date:   2019-01-30T08:19:31+01:00
# @Email:  qlaborde@evertygo.com
# @Last modified by:   laborde
# @Last modified time: 2019-01-30T11:23:27+01:00

#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import requests

CONFIG_INI = "config.ini"

class ImperiHome(object):

    def __init__(self):
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            self.config = None

        # start listening to MQTT
        self.start_blocking()

    ############### Sub callback functions ###############

    # Get app code version
    def about_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)


        IP =  self.config.get("global").get("IP")

        # url = "http://192.168.10.185:8080/api/rest/imperihome/about"
        url = "http://"+IP+":8080/api/rest/imperihome/about"

        data = requests.get(url).json();

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "Application code version : " + str(data.get("versionCode")), "")

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'evertygo:about':
            self.about_callback(hermes, intent_message)

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes("localhost:1883") as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    ImperiHome()
