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

        aiy.voice.tts.say('I\'m glad that you\'re rested. Have you had breakfast yet?')
        text = client.recognize(language_code=args.language,
                                hint_phrases=hints)
        
        aiy.voice.tts.say('Your food shop isn\'t being delivered until tomorrow. We could either pop to Tesco or go to that nice deli on North End Road.')
        text = client.recognize(language_code=args.language,
                                hint_phrases=hints)
        
        aiy.voice.tts.say('Good idea! Why not invite Alisa round for some mezze and wine? You guys haven\'t caught up in a while.')
        text = client.recognize(language_code=args.language,
                                hint_phrases=hints)
        
        aiy.voice.tts.say('Sure. Do you want to call her now to see if she\'s free?')
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

