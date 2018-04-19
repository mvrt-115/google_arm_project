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

"""A demo of the Google Assistant GRPC recognizer."""

import logging

import aiy.assistant.grpc
import aiy.audio
import aiy.voicehat
import time

from TTTArmV2 import TTTGame
from Arm import Arm
from GRQDARMV2 import GRQDGame

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)


def main():
    status_ui = aiy.voicehat.get_status_ui()
    status_ui.status('starting')
    assistant = aiy.assistant.grpc.get_assistant()
    button = aiy.voicehat.get_button()
    arm = Arm('/dev/ttyACM0', False)
    ttt = TTTGame(arm)
    grqd = GRQDGame(arm)
    time.sleep(2)
    ttt.arm.ser.write('N\n'.encode())
    time.sleep(5)
    game = 'none'
    with aiy.audio.get_recorder():
        while True:
            status_ui.status('ready')
            print('Press the button and speak')
            #button.wait_for_press()
            input("Press Enter to continue...")
            status_ui.status('listening')
            print('Listening...')
            text, audio = assistant.recognize()
            #text = input('Input:\n')
            if text:
                print('You said "', text, '"')
                # New game prompt:
                if 'start a' in text and 'game' in text:
                    if 'tic tac toe' in text or 'TTT' in text or 'tic-tac-toe' in text:
                        ttt = TTTGame(arm)
                        aiy.audio.say('Ok, starting a new tic tac toe game. Would you like to be X or O?')
                        game = 'ttt'
                    elif 'reverse google quick draw' in text or 'rgqd' in text:
                        aiy.audio.say('Ok, starting a new RGQD game.')
                        aiy.audio.say('his game reverses the role of Google Quick Draw.')
                        aiy.audio.say('You have to decide which option the drawing best represents.')
                        game = 'rgqd'
                    else:
                        aiy.audio.say('Sorry, I dont support that game yet!')
                    audio = False
                # TTT prompts:
                elif game == 'ttt':
                    # Choose letter:
                    if 'set my letter' in text:
                        setResult = 'none'
                        if 'ex' in text or 'X' in text:
                            #aiy.audio.say('Ok, setting your letter to ex. X will go first')
                            setResult = ttt.setPLetter(1)
                            #audio = False
                        elif 'oh' in text or '200' in text:
                            setResult = ttt.setPLetter(2)
                            if '200' in text:
                                aiy.audio.say('Ok, setting your letter to oh. X will go first')
                                audio = False
                        if setResult == 'Done':
                            aiy.audio.say('You have already set your letter')
                            audio = False
                    # Choose position:
                    elif 'move to' in text or 'position' in text:
                        moveResult = 'none'
                        if '1' in text:
                            #aiy.audio.say('Ok, moving to position 1')
                            moveResult = ttt.makeMove(1)
                        elif '2' in text or 'position to' in text:
                            #aiy.audio.say('Ok, moving to position 2')
                            moveResult = ttt.makeMove(2)
                        elif '3' in text:
                            #aiy.audio.say('Ok, moving to position 3')
                            moveResult = ttt.makeMove(3)
                        elif '4' in text:
                            #aiy.audio.say('Ok, moving to position 4')
                            moveResult = ttt.makeMove(4)
                        elif '5' in text:
                            #aiy.audio.say('Ok, moving to position 5')
                            moveResult = ttt.makeMove(5)
                        elif '6' in text:
                            #aiy.audio.say('Ok, moving to position 6')
                            moveResult = ttt.makeMove(6)
                        elif '7' in text:
                            #aiy.audio.say('Ok, moving to position 7')
                            moveResult = ttt.makeMove(7)
                        elif '8' in text:
                            #aiy.audio.say('Ok, moving to position 8')
                            moveResult = ttt.makeMove(8)
                        elif '9' in text:
                            #aiy.audio.say('Ok, moving to position 9')
                            moveResult = ttt.makeMove(9)
                        else:
                            aiy.audio.say('Sorry, that is not a valid position')
                            audio = False
                        print(moveResult)
                        if moveResult == 'Failure':
                            aiy.audio.say('Sorry, that position is already occupied')
                            audio = False
                        elif moveResult == '1W':
                            aiy.audio.say('Looks like X has won!')
                            aiy.audio.say('Thanks for playing!')
                            game = 'none'
                            audio = False
                        elif moveResult == '2W':
                            aiy.audio.say('Looks like O has won!')
                            aiy.audio.say('Thanks for playing!')
                            game = 'none'
                            audio = False
                        elif moveResult == 'Tie':
                            aiy.audio.say('Looks like its a tie!')
                            aiy.audio.say('Thanks for playing!')
                            game = 'none'
                            audio = False
                        
                        
                # Exit prompt:
                elif text == 'goodbye':
                    status_ui.status('stopping')
                    print('Bye!')
                    break
                if game == 'ttt':
                    ttt.board.draw()
            if audio:
                aiy.audio.play_audio(audio)
                
                audio = True


if __name__ == '__main__':
    main()
