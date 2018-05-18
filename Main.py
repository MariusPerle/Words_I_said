import atexit
import configparser
import os
import sys
from threading import Thread

import speech_recognition as sr


def mainfunction(source, args):
    audio = r.listen(source, phrase_time_limit=2)
    try:
        user = r.recognize_google(audio, language=args['language'])
    except sr.UnknownValueError:
        user = ''
    thread = Thread(target=using_it, args=(user,))
    thread.start()
    if args['end_statement']:
        if args['end_statement'] in user:
            sys.exit('shutdown')


def using_it(text):
    print(text)
    words = text.split(' ')
    for entry in words:
        if entry in ['', ' ']:
            continue
        if entry in list_all_words.keys():
            list_all_words[entry] += 1
        else:
            list_all_words[entry] = 1
    print(list_all_words)


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    end =config['DEFAULT']['end_statement']
    if end is '':
        end = None
    return {'language':config['DEFAULT']['language'],
            'end_statement':end,}




if __name__ == "__main__":
    list_all_words = {}
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while 1:
            mainfunction(source, read_config())