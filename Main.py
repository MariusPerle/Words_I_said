import configparser
import operator
import sys
import tkinter as tk
from threading import Thread

import speech_recognition as sr


class GUI:
    def __init__(self, master, config):
        self.label = tk.Label(master)
        self.label.grid(row=0, column=0)
        self.label.configure(text='nothing')
        self.update_label()

    def update_label(self):
        if list_all_words is not {}:
            if config_args['amount_shown'] is '':
                text = count_one_word(config_args['count_this_word'])
            else:
                text = most_frequent_words(config_args)
            self.label.configure(text=text)
            self.label.after(1000, self.update_label)  # call this method again in 1,000 milliseconds


def voice_2_text(source, config):
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source, phrase_time_limit=1)
    thread = Thread(target=text_analysis, args=(audio, config))
    thread.start()


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


def text_analysis(audio, config):
    try:
        text = r.recognize_google(audio, language=config['language'])
    except sr.UnknownValueError:
        return
    print(text)
    our_text.append(text)
    text = text.lower()
    words = text.split(' ')
    for entry in words:
        if entry in ['', ' ']:
            continue
        if entry in list_all_words.keys():
            list_all_words[entry] += 1
        else:
            list_all_words[entry] = 1
    if config['end_statement']:
        save_text(text, config)


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    end = config['DEFAULT']['end_statement']

    if end is '':
        end = None
    return {'language': config['DEFAULT']['language'],
            'end_statement': end,
            'amount_shown': config['GUI']['amount_shown'],
            'count_this_word': config['GUI']['count_this_word']}


def run_gui(config):
    root = tk.Tk()
    GUI(root, config)
    root.mainloop()


def most_frequent_words(config):
    sorted_map = sorted(list_all_words.items(), key=operator.itemgetter(1), reverse=True)
    text = ''
    count = 0
    for k in sorted_map:
        if count < int(config['amount_shown']):
            text += k[0] + '\t ' + str(list_all_words[k[0]])
            text += '\n'
            count += 1
        else:
            continue
    return text


def count_one_word(word):
    if word in list_all_words.keys():
        return word + '  ' + str(list_all_words[word])
    else:
        return word


if __name__ == "__main__":
    our_text = []
    list_all_words = {}
    r = sr.Recognizer()
    config_args = read_config()
    thread = Thread(target=run_gui, args=(config_args,))
    thread.start()
    with sr.Microphone() as source:
        while True:
            voice_2_text(source, config_args)
