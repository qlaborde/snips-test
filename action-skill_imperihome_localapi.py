#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
from translations import translations

import io
import requests
import json

CONFIG_INI = "config.ini"

class ImperiHome(object):

    def __init__(self):
        # Get config
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            print 'Error : can\'t load config'
            self.config = None

        # Get translations json
        try:
            self.t = json.loads(json.dumps(translations))
        except :
            print 'Error : can\'t load translations'
            self.t = None

        # start listening to MQTT
        if self.config != None and self.t != None:
            self.start_blocking()
        else:
            print 'Error : can\'t start blocking'

    ############### Sub callback functions ###############

    # Get app code version
    def getInfo_callback(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        ip = self.config.get('secret').get('ip')
        port = self.config.get('secret').get('port')
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
                print 'temp found'
                hermes.publish_end_session(intent_message.session_id, data.get("temp").get("message"))
            elif data != None and 'error' in data:
                print 'error found'
                hermes.publish_end_session(intent_message.session_id, data.get("error").get("message"))
            else:
                hermes.publish_end_session(intent_message.session_id, self.t[self.lang]['error_temp_data'])
        except Exception as e:
            print('getTemp_callback error = ' + str(e))
            hermes.publish_end_session(intent_message.session_id, self.t[self.lang]['error_temp_unknown'])

    def getHum_callback(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        try:
            device_name = self.getDeviceName(intent_message)
            data = self.getData(device_name)
            if data != None and 'hum' in data:
                hermes.publish_end_session(intent_message.session_id, data.get("hum").get("message"))
            elif data != None and 'error' in data:
                hermes.publish_end_session(intent_message.session_id, data.get("error").get("message"))
            else:
                hermes.publish_end_session(intent_message.session_id, self.t[self.lang]['error_hum_data'])
        except Exception as e:
            print('e = ' + str(e))
            hermes.publish_end_session(intent_message.session_id, self.t[self.lang]['error_hum_unknown'])

    def getStatus_callback(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        try:
            device_name = self.getDeviceName(intent_message)
            data = self.getData(device_name)
            if data != None and 'status' in data:
                hermes.publish_end_session(intent_message.session_id, data.get("status").get("message"))
            elif data != None and 'error' in data:
                hermes.publish_end_session(intent_message.session_id, data.get("error").get("message"))
            else:
                hermes.publish_end_session(intent_message.session_id, self.t[self.lang]['error_status_data'])
        except Exception as e:
            print('e = ' + str(e))
            hermes.publish_end_session(intent_message.session_id, self.t[self.lang]['error_status_unknown'])

    def getLevel_callback(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        try:
            device_name = self.getDeviceName(intent_message)
            data = self.getData(device_name)
            if data != None and 'level' in data:
                hermes.publish_end_session(intent_message.session_id, data.get("level").get("message"))
            elif data != None and 'error' in data:
                hermes.publish_end_session(intent_message.session_id, data.get("error").get("message"))
            else:
                hermes.publish_end_session(intent_message.session_id, self.t[self.lang]['error_level_data'])
        except Exception as e:
            print('e = ' + str(e))
            hermes.publish_end_session(intent_message.session_id, self.t[self.lang]['error_level_unknown'])

    def setStatus_callback(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        try:
            device_name = self.getDeviceName(intent_message)

            action = None
            if len(intent_message.slots.status) > 0:
                action = intent_message.slots.status.first().value
                action = self.formatValue(action)
            elif len(intent_message.slots.action) > 0:
                action = intent_message.slots.action.first().value
                action = self.formatValue(action)

            data = self.executeAction(u"setStatus", device_name, action);

            if data != None and 'status' in data and 'message' in data:
                hermes.publish_end_session(intent_message.session_id, data.get("message"))
            elif data != None and 'error' in data:
                hermes.publish_end_session(intent_message.session_id, data.get("error").get("message"))
            else:
                hermes.publish_end_session(intent_message.session_id, self.t[self.lang]['error_set_status'])
        except Exception as e:
            print('e = ' + str(e))
            hermes.publish_end_session(intent_message.session_id, self.t[self.lang]['error_set_status_unknown'])

    def setLevel_callback(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        try:
            device_name = self.getDeviceName(intent_message)

            value = None
            if len(intent_message.slots.value) > 0:
                value = intent_message.slots.value.first().value

            data = self.executeAction(u"setLevel", device_name, value);

            if data != None and 'level' in data and 'message' in data :
                hermes.publish_end_session(intent_message.session_id, data.get("message"))
            elif data != None and 'error' in data:
                hermes.publish_end_session(intent_message.session_id, data.get("error").get("message"))
            else:
                hermes.publish_end_session(intent_message.session_id, self.t[self.lang]['error_set_level'])
        except Exception as e:
            print('e = ' + str(e))
            hermes.publish_end_session(intent_message.session_id, self.t[self.lang]['error_set_level_unknown'])

    def setColor_callback(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        try:
            device_name = self.getDeviceName(intent_message)

            color = None
            if len(intent_message.slots.color) > 0:
                color = intent_message.slots.color.first().value

            data = self.executeAction(u"setColor", device_name, color);

            if data != None and 'color' in data and 'message' in data :
                hermes.publish_end_session(intent_message.session_id, data.get("message"))
            elif data != None and 'error' in data:
                hermes.publish_end_session(intent_message.session_id, data.get("error").get("message"))
            else:
                hermes.publish_end_session(intent_message.session_id, self.t[self.lang]['error_set_color'])
        except Exception as e:
            print('e = ' + str(e))
            hermes.publish_end_session(intent_message.session_id, self.t[self.lang]['error_set_color_unknown'])

    def setShutter_callback(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        try:
            device_name = self.getDeviceName(intent_message)

            level = None
            if len(intent_message.slots.action) > 0:
                action = intent_message.slots.action.first().value
                level = self.formatValue(action)

            data = self.executeAction(u"setLevel", device_name, level);

            if data != None and 'level' in data and 'message' in data :
                hermes.publish_end_session(intent_message.session_id, data.get("message"))
            elif data != None and 'error' in data:
                hermes.publish_end_session(intent_message.session_id, data.get("error").get("message"))
            else:
                hermes.publish_end_session(intent_message.session_id, self.t[self.lang]['error_set_position'])
        except Exception as e:
            print('e = ' + str(e))
            hermes.publish_end_session(intent_message.session_id, self.t[self.lang]['error_set_position_unknown'])

    def getData(self, name):
        print('getData')
        try:
            print("name = " + name.encode("utf-8"))
            ip = self.config.get('secret').get('ip')
            port = self.config.get('secret').get('port')
            lang = self.lang
            url = u"http://" + ip + u":"+ port + u"/api/rest/devices/data?name=" + name + u"&lang=" + lang
            # print("type url = " + str(type(url)))
            print("url = " + url.encode("utf-8"))
            data = requests.get(url, timeout=2).json()
            print('data = ' + str(data))
            return data
        except Exception as e:
            print('getData error = ' + str(e))
            return None

    def executeAction(self, action, name, value):
        print('executeAction')
        try:
            ip = self.config.get('secret').get('ip')
            port = self.config.get('secret').get('port')
            lang = self.lang
            url = u"http://" + ip + u":" + port + u"/api/rest/devices/action/"+ action + u"?name=" + name + u"&lang=" + lang
            print("type url = " + str(type(url)))
            if value != None:
                url = url + u"&value=" + str(value).decode('utf-8')

            print('url = ' + url.encode("utf-8"))
            data = requests.post(url, timeout=2).json()
            return data
        except Exception as e:
            print('executeAction error = ' + str(e))
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

        self.lang = u'en'
        if coming_intent.endswith('fr'):
            self.lang = u'fr'

        if coming_intent.startswith('evertygo:getInfo'):
            self.getInfo_callback(hermes, intent_message)
        if coming_intent.startswith('evertygo:getTemp'):
            self.getTemp_callback(hermes, intent_message)
        if coming_intent.startswith('evertygo:getHum'):
            self.getHum_callback(hermes, intent_message)
        if coming_intent.startswith('evertygo:getStatus'):
            self.getStatus_callback(hermes, intent_message)
        if coming_intent.startswith('evertygo:getLevel'):
            self.getLevel_callback(hermes, intent_message)
        if coming_intent.startswith('evertygo:setStatus'):
            self.setStatus_callback(hermes, intent_message)
        if coming_intent.startswith('evertygo:setLevel'):
            self.setLevel_callback(hermes, intent_message)
        if coming_intent.startswith('evertygo:setColor'):
            self.setColor_callback(hermes, intent_message)
        if coming_intent.startswith('evertygo:setShutter'):
            self.setShutter_callback(hermes, intent_message)

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes("localhost:1883") as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    ImperiHome()
