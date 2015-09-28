# -*- coding: utf-8 -*-
"""
Created on Tue Sep 01 15:49:04 2015

@author: asus
"""

import requests
import re
import sys
import time
import urllib2
import ssl
import Skype4Py

ssl._create_default_https_context = ssl._create_unverified_context
reload(sys)
sys.setdefaultencoding('utf-8')

def query_tick(date,from_station,to_station,skype_instance):

	
    try:
        url='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date='+date+'&leftTicketDTO.from_station='+from_station+'&leftTicketDTO.to_station='+to_station+'&purpose_codes=ADULT'
    except:
        print 'network run into problem..........................'
        return
    response=urllib2.urlopen(url)
    html=response.read()
    
    pattern_train_number=re.compile('station_train_code":".{2,5}"')
    train_number=pattern_train_number.findall(html)
    train_number=[a.split('"')[-2] for a in train_number]
    
    pattern_start_time=re.compile('"start_time":"\d{1,2}:\d{1,2}"')
    start_time=pattern_start_time.findall(html)
    start_time=[a.split('"')[-2] for a in start_time]
    
    pattern_tick_number=re.compile('"ze_num":"(\xe6\x97\xa0|\d{1,4}|\xe6\x9c\x89)"')
    tick_number=pattern_tick_number.findall(html)
    
    for i in range(len(train_number)):
        print date,train_number[i],start_time[i],tick_number[i],time.strftime("%H:%M:%S")
        #skype_instance.send_message([date,train_number[i],start_time[i],tick_number[i],time.strftime("%H:%M:%S")])    
        
        if tick_number[i]!='\xe6\x97\xa0':
            skype_instance.send_message([date,train_number[i],start_time[i],tick_number[i],time.strftime("%H:%M:%S")])
            skype_instance.call_the_body()


class skype:
    
    def __init__(self):
        self.skypecon=Skype4Py.Skype()
        self.skypecon.Attach()
        self.client_Phone='songqiskype'
    
    def call_the_body(self):
        m_call=self.skypecon.PlaceCall(self.client_Phone)
    
    def send_message(self,message):
        m_mes=self.skypecon.SendMessage(self.client_Phone,message)
        
                    


    
    
songqi=skype()

while True:
    
    query_tick('2015-10-01','BJP','JVK',songqi)
    query_tick('2015-10-04','JVK','BJP',songqi)
    time.sleep(0.5)
