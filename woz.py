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
import time

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
        name= 'Mary'
        aiy.voice.tts.say('Hi there'+str(name)+'nice to meet you')
        time.sleep(0.5)
        aiy.voice.tts.say('sorry if i did not pronounce that correctly, I am always learning')
        time.sleep(0.5)
        aiy.voice.tts.say('Could you tell me your personality type, this is so I get to know you better. just say the four letters')
        text = client.recognize(language_code=args.language,
                                hint_phrases=hints)
        psn= input()
        aiy.voice.tts.say('Oh thank you so you are type'+str(psn[0]))
        time.sleep(0.5)
        aiy.voice.tts.say(str(psn[1]))
        time.sleep(0.5)
        aiy.voice.tts.say(str(psn[2]))
        time.sleep(0.5)
        aiy.voice.tts.say(str(psn[3]))
        time.sleep(0.5)
        aiy.voice.tts.say('Wait a second, I need to configure my settings for you')
        time.sleep(0.5)
        aiy.voice.tts.say('Let us talk. So how have you been lately?')
        text = client.recognize(language_code=args.language,
                                hint_phrases=hints)
        
        convo_finished=False
        while convo_finished!=True:
            amica= input()
            aiy.voice.tts.say(str(amica))
        
if __name__ == '__main__':
    main()

