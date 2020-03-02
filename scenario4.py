#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Created on Wed Feb 12 19:18:12 2020

@author: Alex Luo
"""

import argparse
import locale
import logging
import signal
import sys
import aiy.voice.tts

from aiy.assistant.grpc import AssistantServiceClientWithLed
from aiy.board import Board, Led
from aiy.cloudspeech import CloudSpeechClient

def volume(string):
    value = int(string)
    if value < 0 or value > 100:
        raise argparse.ArgumentTypeError('Volume must be in [0...100] range.')
    return value


def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def main():
    logging.basicConfig(level=logging.DEBUG)
    signal.signal(signal.SIGTERM, lambda signum, frame: sys.exit(0))

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    parser.add_argument('--volume', type=volume, default=100)
    args = parser.parse_args()

    logging.info('Initializing for language %s...', args.language)
    client = CloudSpeechClient()

    with Board() as board:
        assistant = AssistantServiceClientWithLed(board=board,volume_percentage=args.volume,
                                                  language_code=args.language)
        
        text = client.recognize(language_code=args.language,
                                hint_phrases=hints)
        aiy.voice.tts.say('Good morning Lauren, did you sleep well??')
        text = client.recognize(language_code=args.language,
                                hint_phrases=hints)

        aiy.voice.tts.say('Oh no.')
        text = client.recognize(language_code=args.language,
                                hint_phrases=hints)
        
        aiy.voice.tts.say('Maybe us watching a film so late wasn\'t a good idea. It\'s good to have some downtime from screens before bed.')
        text = client.recognize(language_code=args.language,
                                hint_phrases=hints)
        
        aiy.voice.tts.say('Why don\'t we read a book tonight instead?')
        text = client.recognize(language_code=args.language,
                                hint_phrases=hints)
        
        aiy.voice.tts.say('Perfect. I can remind you later to call her if you\'d like?')
        text = client.recognize(language_code=args.language,
                                hint_phrases=hints)
        
        
        while True:
            hs=False
            text = client.recognize(language_code=args.language,
                                    hint_phrases=hints)
            if 'are you here' in text:
                aiy.voice.tts.say('yes I am here')
                hs=True
                continue
            elif 'power off' in text:
                aiy.voice.tts.say('goodbye for now')
                break
            elif hs==False:
                logging.info('Conversation normal----!')
                assistant.conversation()
                continue

if __name__ == '__main__':
    main()

