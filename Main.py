import configparser
import sys
from threading import Thread

import speech_recognition as sr


def voice_2_text(source, args):
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source, phrase_time_limit=2)
    try:
        user = r.recognize_google(audio, language=args['language'])
    except sr.UnknownValueError:
        user = ''
    thread = Thread(target=using_it, args=(user,))
    thread.start()
    if args['end_statement']:
        save_text(user, args)


def save_text(user, config):
    if config['end_statement'] in user:
        with open('text.txt', 'w', encoding='utf-8') as file:
            for line in our_text:
                if line in ['', ' ']:
                    continue
                if line in config['end_statement']:
                    continue
                file.write(line)
                file.write('\n')
        sys.exit('file saved')


def using_it(text):
    print(text)
    our_text.append(text)
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
    end = config['DEFAULT']['end_statement']
    if end is '':
        end = None
    return {'language': config['DEFAULT']['language'],
            'end_statement': end, }


if __name__ == "__main__":
    our_text = []
    list_all_words = {}
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while 1:
            voice_2_text(source, read_config())
