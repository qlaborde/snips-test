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
    def getInfo_callback(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        print('self.config = ' + str(self.config))

        ip = self.config.get('secret').get('ip')
        port = self.config.get('secret').get('port')

        print('ip = ' + str(ip))
        print('port = ' + str(port))

        url = "http://"+ip+":"+port+"/api/rest/imperihome/about"
        print('url = ' + url)
        data = requests.get(url).json();
        hermes.publish_end_session(intent_message.session_id, "I am a "+ str(data.get("device")) +". My version name is "+ str(data.get("versionName")) +" and my version code is " + str(data.get("versionCode")))

    def getTemp_callback(self, hermes, intent_message):
        # hermes.publish_end_session(intent_message.session_id)
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        try:
            device_name = self.getDeviceName(intent_message)

            data = self.getData(device_name)
            if data != None and 'temp' in data:
                hermes.publish_end_session(intent_message.session_id, str(data.get("temp").get("message")))
            elif data != None and 'error' in data:
                hermes.publish_end_session(intent_message.session_id, str(data.get("error").get("message")))
            else:
                print('device_name = ' + device_name)
                hermes.publish_end_session(intent_message.session_id, "Sorry, I can't get the device temperature 1")
        except Exception as e:
            print('e = ' + str(e))
            hermes.publish_end_session(intent_message.session_id, "Sorry, I can't get the device temperature 2")

    def getHum_callback(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        try:
            device_name = self.getDeviceName(intent_message)
            data = self.getData(device_name)
            if data != None and 'hum' in data:
                hermes.publish_end_session(intent_message.session_id, str(data.get("hum").get("message")))
            elif data != None and 'error' in data:
                hermes.publish_end_session(intent_message.session_id, str(data.get("error").get("message")))
            else:
                hermes.publish_end_session(intent_message.session_id, "Sorry, I can't get the device humidity 1")
        except Exception as e:
            print('e = ' + str(e))
            hermes.publish_end_session(intent_message.session_id, "Sorry, I can't get the device humidity 2")

    def getStatus_callback(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        try:
            device_name = self.getDeviceName(intent_message)
            data = self.getData(device_name)
            if data != None and 'status' in data:
                hermes.publish_end_session(intent_message.session_id, data.get("status").get("message"))
            elif data != None and 'error' in data:
                hermes.publish_end_session(intent_message.session_id, str(data.get("error").get("message")))
            else:
                hermes.publish_end_session(intent_message.session_id, "Sorry, I can't get the device status 1")
        except Exception as e:
            print('e = ' + str(e))
            hermes.publish_end_session(intent_message.session_id, "Sorry, I can't get the device status 2")

    def getLevel_callback(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        try:
            device_name = self.getDeviceName(intent_message)
            data = self.getData(device_name)
            if data != None and 'level' in data:
                hermes.publish_end_session(intent_message.session_id, data.get("level").get("message"))
            elif data != None and 'error' in data:
                hermes.publish_end_session(intent_message.session_id, str(data.get("error").get("message")))
            else:
                hermes.publish_end_session(intent_message.session_id, "Sorry, I can't get the device level 1")
        except Exception as e:
            print('e = ' + str(e))
            hermes.publish_end_session(intent_message.session_id, "Sorry, I can't get the device status 2")

    def setStatus_callback(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        try:
            device_name = self.getDeviceName(intent_message)

            status = None
            if len(intent_message.slots.status) > 0:
                status = intent_message.slots.status.first().value
                status = self.formatValue(status)

            data = self.executeAction("setStatus", device_name, status);

            if data != None and 'status' in data and 'message' in data:
                hermes.publish_end_session(intent_message.session_id, str(data.get("message")))
            elif data != None and 'error' in data:
                hermes.publish_end_session(intent_message.session_id, str(data.get("error").get("message")))
            else:
                hermes.publish_end_session(intent_message.session_id, "Sorry, I can't switch the device 1")
        except Exception as e:
            print('e = ' + str(e))
            hermes.publish_end_session(intent_message.session_id, "Sorry, I can't switch the device 2")

    def setLevel_callback(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        try:
            device_name = self.getDeviceName(intent_message)

            value = None
            if len(intent_message.slots.value) > 0:
                value = intent_message.slots.value.first().value

            data = self.executeAction("setLevel", device_name, value);

            if data != None and 'level' in data and 'message' in data :
                hermes.publish_end_session(intent_message.session_id, str(data.get("message")) + " %")
            elif data != None and 'error' in data:
                hermes.publish_end_session(intent_message.session_id, str(data.get("error").get("message")))
            else:
                hermes.publish_end_session(intent_message.session_id, "Sorry, I can't set the device level 1")
        except Exception as e:
            print('e = ' + str(e))
            hermes.publish_end_session(intent_message.session_id, "Sorry, I can't et the device level 2")

    def setColor_callback(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        try:
            device_name = self.getDeviceName(intent_message)

            color = None
            if len(intent_message.slots.color) > 0:
                color = intent_message.slots.color.first().value

            data = self.executeAction("setColor", device_name, color);

            if data != None and 'color' in data and 'message' in data :
                hermes.publish_end_session(intent_message.session_id, str(data.get("message")))
            elif data != None and 'error' in data:
                hermes.publish_end_session(intent_message.session_id, str(data.get("error").get("message")))
            else:
                hermes.publish_end_session(intent_message.session_id, "Sorry, I can't set the device color 1")
        except Exception as e:
            print('e = ' + str(e))
            hermes.publish_end_session(intent_message.session_id, "Sorry, I can't et the device color 2")

    def setShutter_callback(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        try:
            device_name = self.getDeviceName(intent_message)

            level = None
            if len(intent_message.slots.action) > 0:
                action = intent_message.slots.action.first().value
                level = self.formatValue(action)

            data = self.executeAction("setLevel", device_name, level);

            if data != None and 'level' in data and 'message' in data :
                hermes.publish_end_session(intent_message.session_id, str(data.get("message")))
            elif data != None and 'error' in data:
                hermes.publish_end_session(intent_message.session_id, str(data.get("error").get("message")))
            else:
                hermes.publish_end_session(intent_message.session_id, "Sorry, I can't set the device level 1")
        except Exception as e:
            print('e = ' + str(e))
            hermes.publish_end_session(intent_message.session_id, "Sorry, I can't et the device level 2")

    def getData(self, name):
        try:
            ip = self.config.get('secret').get('ip')
            port = self.config.get('secret').get('port')
            url = "http://"+ip+":"+port+"/api/rest/devices/data?name=" + name + "&lang=en"
            print('url = ' + url)
            data = requests.get(url, timeout=2).json()
            print('data = ' + str(data))
            return data
        except Exception as e:
            return None

    def executeAction(self, action, name, value):
        try:
            ip = self.config.get('secret').get('ip')
            port = self.config.get('secret').get('port')
            url = "http://"+ip+":"+port+"/api/rest/devices/action/"+ action +"?name=" + name + "&lang=en"

            if value != None:
                url = url + "&value=" + str(value)

            print('url = ' + url)
            data = requests.post(url, timeout=2).json()
            return data
        except Exception as e:
            return None

    def getDeviceName(self, intent_message):
        try:
            device_name = ""
            if len(intent_message.slots.device) > 0:
                device_name = intent_message.slots.device.first().value
            elif len(intent_message.slots.room) > 0:
                device_name = intent_message.slots.room.first().value
            else:
                device_name = "unknown"

            return device_name
        except Exception as e:
            return "unknown"

    def formatValue(self, value):
        if value == 'on':
            value = '1'
        elif value == 'off':
            value = '0'
        elif value == 'open' or value == 'raise':
            value = '100'
        elif value == 'close':
            value = '0'

        return value

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'evertygo:getInfo':
            self.getInfo_callback(hermes, intent_message)
        if coming_intent == 'evertygo:getTemp':
            self.getTemp_callback(hermes, intent_message)
        if coming_intent == 'evertygo:getHum':
            self.getHum_callback(hermes, intent_message)
        if coming_intent == 'evertygo:getStatus':
            self.getStatus_callback(hermes, intent_message)
        if coming_intent == 'evertygo:getLevel':
            self.getLevel_callback(hermes, intent_message)
        if coming_intent == 'evertygo:setStatus':
            self.setStatus_callback(hermes, intent_message)
        if coming_intent == 'evertygo:setLevel':
            self.setLevel_callback(hermes, intent_message)
        if coming_intent == 'evertygo:setColor':
            self.setColor_callback(hermes, intent_message)
        if coming_intent == 'evertygo:setShutter':
            self.setShutter_callback(hermes, intent_message)

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes("localhost:1883") as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    ImperiHome()
