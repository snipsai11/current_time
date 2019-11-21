#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import random

from assistant import Assistant

# ======================================================================================================================

assist = Assistant()
jokes = None
file_path = os.path.dirname(os.path.realpath(__file__)) + "/"


# ======================================================================================================================

def load_jokes(lang, safe_only=False):
    if (safe_only):
        path = file_path + "jokes/" + lang.lower() + "_safe_only.txt"
    else:
        path = file_path + "jokes/" + lang.lower() + ".txt"

    with open(path, encoding="utf-8") as file:
        # Read line by line and remove whitespace characters at the end of each line
        content = file.readlines()
        content = [x.strip() for x in content]

    random.shuffle(content)
    return content


# ======================================================================================================================

def get_joke():
    """ Get first entry and append it to the end -> no repetition until every entry selected """

    joke = jokes.pop(0)
    jokes.append(joke)
    return joke


# ======================================================================================================================

def callback_tell_joke(hermes, intent_message):
    result_sentence = "Das Bild wurde erfolgreich abgespeichert"
# result_sentence = get_joke()
    hermes.publish_end_session(intent_message.session_id, result_sentence)


# ======================================================================================================================

jokes = load_jokes(assist.get_config()["secret"]["language"],
                   assist.get_config()["secret"]["safe_jokes_only"] == "true")

if __name__ == "__main__":
    h = assist.get_hermes()
    h.connect()
    h.subscribe_intent("DANBER:tellJoke", callback_tell_joke)
    h.loop_forever()