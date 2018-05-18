from threading import Thread

import pyaudio,os
import speech_recognition as sr
import configparser


def excel():
        os.system("start excel.exe")

def internet():
        os.system("start chrome.exe")

def media():
        os.system("start wmplayer.exe")

def mainfunction(source, language):
    audio = r.listen(source)
    try:
        user = r.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        user = ''
    thread = Thread(target=using_it, args=(user, ))
    thread.start()
    thread.join()
    if user == "Excel":
        excel()
    elif user == "Internet":
        internet()
    elif user == "music":
        media()

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
    return config['DEFAULT']['language']

if __name__ == "__main__":
    list_all_words = {}
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while 1:
            mainfunction(source, read_config())
