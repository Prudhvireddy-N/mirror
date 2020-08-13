#!/usr/bin/env python3


import logging
import platform
import sys
import subprocess 
import requests
import time
import aiy.voice.audio
from google.assistant.library.event import EventType
from aiy.assistant import auth_helpers
from aiy.assistant.library import Assistant
from aiy.board import Board, Led
import argparse
import locale
from aiy.cloudspeech import CloudSpeechClient



origin= ''
dest = ''
zoomflag=0
changezoomstate=0

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language
    
def detail_news(news_client):
    while(1):
        logging.info('News in detail running...')
        text = news_client.recognize()
        if text is None:
            continue
        elif ((text.find('news')!=-1 or text.find('article')!=-1) and (text.find('previous')!=-1)):
            previous_news()
        elif ((text.find('news')!=-1 or text.find('article')!=-1) and (text.find('next')!=-1)):
            next_news()
        elif(text.find('minimise')!=-1 or text.find('minimize')!=-1 or text.find('close')!=-1 or ((text.find('normal')!=-1 or text.find('default')!=-1) and (text.find('view')!=-1 or text.find('display')!=-1))):
            unzoom_module()
            break
        else:
            continue
    

def process_event(text,assistant,board,client):
    
    try:
            global zoomflag
            global changezoomstate
            logging.info('You said:'+text)
            text = text.lower()
            if(text.find('power off')!=-1 or text.find('shut down')!=-1 or text.find('power down')!=-1 or text.find('kill power')!=-1):
                power_off_pi()
            
            elif ((text.find('clock')!=-1 or text.find('time')!=-1) and (text.find('close')!=-1 or  text.find('hide')!=-1 or  text.find('HYD')!=-1)):
                changezoomstate=1
                close_clock()
            
            elif (text.find('clock')!=-1 or text.find('time')!=-1): 
                if (text.find('show')!=-1 or  text.find('open')!=-1 or  text.find('get')!=-1):
                    changezoomstate=1
                    show_clock()
                elif (text.find('tell')!=-1 or text.find('what')!=-1):
                    changezoomstate=1
                    assistant.send_text_query(text)
                    if(zoomflag==1):
                        unzoom_module()
                    show_clock()
                    zoom_clock_timer()
                elif (text.find('zoom')!=-1 or text.find('expand')!=-1 or text.find('maximize')!=-1 or text.find('maximise')!=-1):
                    assistant.stop_conversation()
                    if(zoomflag==1):
                        unzoom_module()
                    zoom_clock()
                    show_clock()
                    changezoomstate=0
                    zoomflag=1
            
            elif ((text.find('map')!=-1 )and (text.find('show')!=-1 or  text.find('open')!=-1 or  text.find('get')!=-1 or text.find('tell')!=-1 or text.find('what')!=-1)):
                show_map()
                changezoomstate=1
            
            elif ((text.find('map')!=-1 )and (text.find('HYD')!=-1 or  text.find('hide')!=-1 or  text.find('close')!=-1)):
                close_map()
                changezoomstate=1
            
            elif ((text.find('weather')!=-1) and (text.find('close')!=-1 or  text.find('hide')!=-1 or  text.find('HYD')!=-1)):
                close_weather()
                changezoomstate=1
            
            
            elif (text.find('weather')!=-1):
                if (text.find('show')!=-1 or  text.find('open')!=-1 or text.find('get')!=-1):
                    show_weather()
                    changezoomstate=1
                elif (text.find('what')!=-1 or text.find('tell')!=-1):
                    assistant.send_text_query(text)
                    show_weather()
                    if(zoomflag==1):
                        unzoom_module()
                    zoom_weather_timer()
                    changezoomstate=1
                elif (text.find('zoom')!=-1 or text.find('expand')!=-1 or text.find('maximize')!=-1 or text.find('maximise')!=-1):
                    assistant.stop_conversation()
                    if(zoomflag==1):
                        unzoom_module()
                    changezoomstate=0
                    zoom_weather()
                    show_weather()
                    zoomflag=1
            
            
            elif ((text.find('calendar')!=-1 ) and (text.find('show')!=-1 or  text.find('open')!=-1 or  text.find('get')!=-1 or text.find('tell')!=-1 or text.find('what')!=-1)):
                show_calendar()
                changezoomstate=1
            
            elif ((text.find('calendar')!=-1) and (text.find('close')!=-1 or  text.find('hide')!=-1 or  text.find('remove')!=-1)):
                close_calendar()
                changezoomstate=1
            
            elif ((text.find('calendar')!=-1) and (text.find('expand')!=-1 or text.find('zoom')!=-1 or  text.find('maximise')!=-1 or  text.find('maximize')!=-1)):
                assistant.stop_conversation()
                if(zoomflag==1):
                    unzoom_module()
                changezoomstate=0
                zoom_calendar()
                show_calendar()
                zoomflag=1
            
            
            
            elif ((text.find('news')!=-1) and (text.find('close')!=-1 or  text.find('hide')!=-1 or  text.find('HYD')!=-1)):
                close_news()
                changezoomstate=1
            
            elif ((text.find('news')!=-1) and (text.find('zoom')!=-1 or  text.find('expand')!=-1 or  text.find('maximize')!=-1 or text.find('maximise')!=-1 or text.find('detail')!=-1)):
                if(zoomflag==1):
                    unzoom_module()
                zoomflag=1
                zoom_news()
                detail_news(client)
                show_news()
                changezoomstate=1
            
            elif ((text.find('news')!=-1) and (text.find('show')!=-1 or  text.find('open')!=-1 or  text.find('get')!=-1 or text.find('tell')!=-1 or text.find('what')!=-1)):
                show_news()
                changezoomstate=1
            
            elif ((text.find('news')!=-1 or text.find('article')!=-1) and (text.find('previous')!=-1)):
                previous_news()
            
            elif ((text.find('news')!=-1 or text.find('article')!=-1) and (text.find('next')!=-1)):
                next_news()
            
            elif ((text.find('map')!=-1 or text.find('directions')!=-1) and (text.find('expand')!=-1 or text.find('zoom')!=-1 or  text.find('maximise')!=-1 or  text.find('maximize')!=-1)):
                assistant.stop_conversation()
                if(zoomflag==1):
                    unzoom_module()
                changezoomstate=0
                zoomflag=1
                zoom_map()
                show_map()
            
            elif((text.find('all')!=-1 or text.find('everything')!=-1) and (text.find('hide')!=-1 or text.find('close')!=-1)):
                hide_all()
                changezoomstate=1
        
            elif((text.find('all')!=-1 or text.find('everything')!=-1) and (text.find('open')!=-1 or text.find('show')!=-1 or text.find('display')!=-1)):
                show_all()
                changezoomstate=1
                
            elif((text.find('way')!=-1 or text.find('where')!=-1 or text.find('route')!=-1) or (text.find('from')!=-1 and text.find('to')!=-1)): 
                #and (text.find('open')!=-1 or text.find('show')!=-1 or text.find('display')!=-1 or text.find('tell')!=-1)):
                changezoomstate=1
                try:
                    global origin
                    global dest
                    end_index=text.find(' to ')
                    if(text.find('from')!=-1):
                         start_index=text.find('from')+5
                         if start_index<end_index:
                            origin=text[start_index:end_index]
                            dest = text[end_index+4:]
                         else:
                            origin=text[start_index:]
                            dest=text[end_index+4:start_index-6]
                    else:
                         origin='Electronics city,Bangalore'
                         dest = text[end_index+4:]
                    logging.info('Origin: '+origin)
                    logging.info('Destination: '+dest)
                    query_txt = 'route from '+origin+' to '+dest
                    assistant.send_text_query(query_txt)
                    refresh_map(origin,dest)
                    show_map()
                    if(zoomflag==1):
                        unzoom_module()
                    time.sleep(2.5);
                    zoom_map_timer()
                    changezoomstate=1
                except Exception as e:
                    logging.info(e)
        
            elif(text.find('minimise')!=-1 or text.find('minimize')!=-1 or text.find('close')!=-1 or ((text.find('normal')!=-1 or text.find('default')!=-1) and (text.find('view')!=-1 or text.find('display')!=-1))):
                assistant.stop_conversation()
                changezoomstate=1
            
            elif ((text.find('things')!=-1 or text.find('list')!=-1) and (text.find('show')!=-1 or  text.find('open')!=-1 or  text.find('get')!=-1 or text.find('tell')!=-1 or text.find('what')!=-1)):
                show_list_items()
                changezoomstate=1
            
            elif ((text.find('things')!=-1 or text.find('list')!=-1) and (text.find('close')!=-1 or  text.find('hide')!=-1 or  text.find('HYD')!=-1)):
                hide_list_items()
                changezoomstate=1
            
            elif ((text.find('things')!=-1 or text.find('list')!=-1) and (text.find('zoom')!=-1 or  text.find('expand')!=-1 or  text.find('maximize')!=-1 or text.find('maximise')!=-1 or text.find('detail')!=-1)):
                if(zoomflag==1):
                    unzoom_module()
                zoomflag=1
                zoom_list_items()
                show_list_items()
                changezoomstate=0
            elif ((text.find('things')!=-1 or text.find('list')!=-1) and (text.find('add')!=-1)):
                start_index=text.find('add')+4
                end_index = text.find(' to ')
                item=text[start_index:end_index].capitalize()
                logging.info('Adding '+item+' to list..')
                add_item_list(item)
                changezoomstate=1
            elif ((text.find('things')!=-1 or text.find('list')!=-1) and (text.find('remove')!=-1 or text.find('delete')!=-1)):
                start_index=text.find('remove')
                if start_index==-1:
                    start_index=text.find('delete')
                start_index+=7
                end_index = text.find(' from ')
                item=text[start_index:end_index].capitalize()
                logging.info('Deleting '+item+' from list..')
                delete_item_list(item)
                changezoomstate=1
            elif (text.find('add')!=-1):
                start_index=text.find('add')+4
                item=text[start_index:].capitalize()
                logging.info('Adding '+item+' to list..')
                add_item_list(item)
                changezoomstate=1
            elif (text.find('remove')!=-1 or text.find('delete')!=-1):
                start_index=text.find('remove')
                if start_index==-1:
                    start_index=text.find('delete')
                start_index+=7
                item=text[start_index:].capitalize()
                logging.info('Deleting '+item+' to list..')
                delete_item_list(item)
                changezoomstate=1
            elif ((text.find('fix')!=-1 or text.find('book')!=-1) and (text.find('meeting')!=-1 or text.find('appointment')!=-1 or text.find('event')!=-1)):
                assistant.send_text_query(text)
            
            else:
                assistant.send_text_query(text)
                time.sleep(1);
            if zoomflag==1:
                if changezoomstate==1:
                    unzoom_module()
                    changezoomstate=0
            logging.info('ready')
                        
                

    except Exception as e:
        logging.info('Exception '+e)
        
        
        
def power_off_pi():
    subprocess.call('sudo shutdown now', shell=True)

def reboot_pi():
    subprocess.call('sudo reboot', shell=True)

def show_all():
    r = requests.get('http://127.0.0.1:8080/remote?action=SHOW&module=module_0_clock')
    r = requests.get('http://127.0.0.1:8080/remote?action=SHOW&module=module_2_calendar')
    r = requests.get('http://127.0.0.1:8080/remote?action=SHOW&module=module_5_MMM-google-route')
    r = requests.get('http://127.0.0.1:8080/remote?action=SHOW&module=module_3_currentweather')
    r = requests.get('http://127.0.0.1:8080/remote?action=SHOW&module=module_4_weatherforecast')
    r = requests.get('http://127.0.0.1:8080/remote?action=SHOW&module=module_7_newsfeed')
    r = requests.get('http://127.0.0.1:8080/remote?action=SHOW&module=module_9_MMM-ToDoList')
    r = requests.get('http://127.0.0.1:8080/remote?action=SHOW&module=module_1_compliments')
    
    
def hide_all():
    r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_0_clock')
    r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_2_calendar')
    r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_5_MMM-google-route')
    r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_6_MMM-Remote-Control')
    r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_3_currentweather')
    r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_4_weatherforecast')
    r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_7_newsfeed')
    r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_9_MMM-ToDoList')
    r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_1_compliments')
    
def show_clock():
    r = requests.get('http://127.0.0.1:8080/remote?action=SHOW&module=module_0_clock')

def close_clock():
    r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_0_clock')

def zoom_weather():
    r = requests.get('http://127.0.0.1:8080/remote?action=TOGGLE&module=module_3_currentweather&message=zoom')

def zoom_weather_timer():
    r = requests.get('http://127.0.0.1:8080/remote?action=TOGGLE&module=module_3_currentweather&message=zoom&timer=8000')

def zoom_clock():
    r = requests.get('http://127.0.0.1:8080/remote?action=TOGGLE&module=module_0_clock&message=zoom')

def zoom_clock_timer():
    r = requests.get('http://127.0.0.1:8080/remote?action=TOGGLE&module=module_0_clock&message=zoom&timer=4000')
    
def zoom_news():
    r = requests.get('http://127.0.0.1:8080/remote?action=TOGGLE&module=module_7_newsfeed&message=zoom')
    
def previous_news():
    global zoomflag
    r = requests.get('http://127.0.0.1:8080/remote?action=TOGGLE&module=module_7_newsfeed&message=previous')
    if zoomflag==1:
        unzoom_module()
        zoomflag=1
        zoom_news()

def next_news():
    global zoomflag
    r = requests.get('http://127.0.0.1:8080/remote?action=TOGGLE&module=module_7_newsfeed&message=next')
    if zoomflag==1:
        unzoom_module()
        zoomflag=1
        zoom_news()
    
def zoom_calendar():
    r = requests.get('http://127.0.0.1:8080/remote?action=TOGGLE&module=module_2_calendar&message=zoom')


def unzoom_module():
    global zoomflag
    zoomflag=0
    r = requests.get('http://127.0.0.1:8080/remote?action=TOGGLE&message=unzoom')
    
    
def close_weather():
    r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_3_currentweather')
    r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_4_weatherforecast')
    
    
def show_weather():
    r = requests.get('http://127.0.0.1:8080/remote?action=SHOW&module=module_3_currentweather')
    r = requests.get('http://127.0.0.1:8080/remote?action=SHOW&module=module_4_weatherforecast')
    
def close_map():
    r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_5_MMM-google-route')
    
def zoom_map():
    r = requests.get('http://127.0.0.1:8080/remote?action=TOGGLE&module=module_5_MMM-google-route&message=zoom')
    
def show_list_items():
    r = requests.get('http://127.0.0.1:8080/remote?action=SHOW&module=module_9_MMM-ToDoList')

def hide_list_items():
    r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_9_MMM-ToDoList')

def zoom_list_items():
    r = requests.get('http://127.0.0.1:8080/remote?action=TOGGLE&module=module_9_MMM-ToDoList&message=zoom')
    
def add_item_list(item):
    r = requests.get('http://127.0.0.1:8080/remote?action=TOGGLE&module=module_9_MMM-ToDoList&message=edit&command=add&item='+item)

def delete_item_list(item):
    r = requests.get('http://127.0.0.1:8080/remote?action=TOGGLE&module=module_9_MMM-ToDoList&message=edit&command=delete&item='+item)
    
def refresh_map(origin,dest):
    r = requests.get('http://127.0.0.1:8080/remote?action=TOGGLE&module=module_5_MMM-google-route&message=change&origin='+origin+'&destination='+dest)

def zoom_map_timer():
    r = requests.get('http://127.0.0.1:8080/remote?action=TOGGLE&module=module_5_MMM-google-route&message=zoom&timer=5000')
    
def show_map():
    r = requests.get('http://127.0.0.1:8080/remote?action=SHOW&module=module_5_MMM-google-route')

def close_calendar():
    r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_2_calendar')
    
def show_calendar():
    r = requests.get('http://127.0.0.1:8080/remote?action=SHOW&module=module_2_calendar')

def close_news():
    r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_7_newsfeed')
    
    
def show_news():
    r = requests.get('http://127.0.0.1:8080/remote?action=SHOW&module=module_7_newsfeed')
    
def close_compliments():
    r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_1_compliments')

def main():
    logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()
    while(1):
        try:
            r = requests.get('http://127.0.0.1:8080/remote?action=SHOW&module=module_0_clock')
            r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_2_calendar')
            r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_5_MMM-google-route')
            r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_3_currentweather')
            r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_4_weatherforecast')
            r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_6_MMM-Remote-Control')
            r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_7_newsfeed')
            r = requests.get('http://127.0.0.1:8080/remote?action=SHOW&module=module_1_compliments')
            r = requests.get('http://127.0.0.1:8080/remote?action=HIDE&module=module_9_MMM-ToDoList')
            client = CloudSpeechClient()
            print(client)
            credentials = auth_helpers.get_assistant_credentials()
            print(credentials)
            with Board() as board,Assistant(credentials) as assistant:
               print('s')
               assistant.set_mic_mute(True);
               print('ss')
               assistant.start()
               print('sss')
               print('start')
               while(1):
                   #status_ui=aiy.Assistant.get_status_ui()
                   
                   print('coming')
                   board.led.state = Led.ON
                   print('here')
                   text = client.recognize(language_code=args.language)

                   #text="friday"
                   print('hgjhr')
                   if text is None:

                     continue
                   elif text.lower().find('friday')!=-1:
                     board.led.state = Led.ON
                     index=text.lower().find('friday')
                     aiy.voice.audio.play_wav('/home/pi/Smart_Mirror/googlestart.wav')
                     text=text[index+7:]
                     if(len(text)>5):
                        logging.info('Processing..')
                        process_event(text,assistant,board,client)
                     else:
                        while(1):
                           logging.info('Smart Mirror Listening..')
                           text1 = client.recognize(language_code=args.language)
                           
                           if text1 is None:
                              continue
                           else:
                              process_event(text1,assistant,board,client)
                              break
                   elif text.lower().find('minimize')!=-1 or text.lower().find('minimise')!=-1 or text.lower().find('close')!=-1:
                     process_event('minimise',assistant,board,client)
                   else:
                     continue
        except Exception as e:
            print(str(e))
            print('exception caught')
            time.sleep(0.5)      


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.info(e)
        

   





