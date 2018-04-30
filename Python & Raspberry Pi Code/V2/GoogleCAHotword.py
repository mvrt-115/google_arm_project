##!/usr/bin/env python

# Copyright (C) 2017 Google Inc.
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


from __future__ import print_function

import argparse
import os.path
import json

import google.auth.transport.requests
import google.oauth2.credentials

import time

from Arm import Arm
from TTTArmV3 import TTTGame
from GRQDARMV2 import GRQDGame
from google.cloud import texttospeech
from pygame import mixer

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file


DEVICE_API_URL = 'https://embeddedassistant.googleapis.com/v1alpha2'

client = texttospeech.TextToSpeechClient()
arm = Arm("/dev/ttyACM0", True)
arm.aWrite("N")
ttt = TTTGame(arm)
grqd = GRQDGame(arm)
guesses = 4
game = "none"

voice = texttospeech.types.VoiceSelectionParams(language_code='en-US', ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
mixer.init()

def play_audio(toSay):
    response = client.synthesize_speech(toSay, voice, audio_config)
    mixer.music.load(response.audio_content)
    mixer.music.play()

def process_device_actions(event, device_id):
    if 'inputs' in event.args:
        for i in event.args['inputs']:
            if i['intent'] == 'action.devices.EXECUTE':
                for c in i['payload']['commands']:
                    for device in c['devices']:
                        if device['id'] == device_id:
                            if 'execution' in c:
                                for e in c['execution']:
                                    if 'params' in e:
                                        yield e['command'], e['params']
                                    else:
                                        yield e['command'], None


def process_event(event, device_id):
    """Pretty prints events.

    Prints all events that occur with two spaces between each new
    conversation and a single space between turns of a conversation.

    Args:
        event(event.Event): The current event to process.
        device_id(str): The device ID of the new instance.
    """
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        print()

    print(event)

    if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
            event.args and not event.args['with_follow_on_turn']):
        print()
    if event.type == EventType.ON_DEVICE_ACTION:
        for command, params in process_device_actions(event, device_id):
            print('Do command', command, 'with params', str(params))

            if command == "com.acme.commands.start_game":
                gameIn = params['game']
                if gameIn == "TTT":
                    game = "ttt"
                    play_audio("Would you like to be X or O?")
                    ttt.drawBoard()
                elif gameIn == "RGQD":
                    game = "rgqd"
                    grqd.chooseObjects()
                    grqd.generateCoordinates()
                    play_audio("This game reverses the role of Google Quick Draw.")
                    play_audio("You have 4 guesses to choose what the object is:")
                    play_audio("a " + grqd.choices[0] + ", a " + grqd.choices[1] + ", a " + grqd.choices[2] + ", or a " + grqd.choices[3] + ".")
                    grqd.drawObject(grqd.xCoords, grqd.yCoords)

            if command == "com.acme.commands.set_letter":
                letter = params["XorO"]
                if game == "ttt":
                    if letter == "X":
                        ttt.setPLetter(1)
                    elif letter == "O":
                        ttt.setPLetter(2)
                    
            
            if command == "com.acme.commands.choose_position":
                pos = int(params['pos'])
                if game == "ttt":
                    moveResult = ttt.makeMove(pos)
                    if moveResult == "Failure":
                        play_audio("Sorry, that position is already occupied")
                    elif moveResult == "1W":
                        play_audio("Looks like X has won!")
                        play_audio("Thanks for playing!")
                        game = "none"
                    elif moveResult == '2W':
                        play_audio("Looks like O has won!")
                        play_audio("Thanks for playing!")
                        game = "none"
                    elif moveResult == "Tie":
                        play_audio("Looks like its a tie!")
                        play_audio("Thanks for playing!")
                        game = "none"
            
            if command == "com.acme.commands.guess_object":
                if game == "grqd":
                    item = params['object']
                    if item == grqd.item:
                        play_audio("You are correct! Thank you for playing!")
                        guesses = 4
                        game = "none"
                    else:
                        guesses = guesses - 1
                        play_audio("Sorry, that is not correct.")
                        if guesses != 0:
                            play_audio("You have " + str(guesses) + " left.")
                        else:
                            play_audio("The object is a " + grqd.item + ".")
                            guesses = 4
                            game = "none"


def register_device(project_id, credentials, device_model_id, device_id):
    """Register the device if needed.

    Registers a new assistant device if an instance with the given id
    does not already exists for this model.

    Args:
       project_id(str): The project ID used to register device instance.
       credentials(google.oauth2.credentials.Credentials): The Google
                OAuth2 credentials of the user to associate the device
                instance with.
       device_model_id(str): The registered device model ID.
       device_id(str): The device ID of the new instance.
    """
    base_url = '/'.join([DEVICE_API_URL, 'projects', project_id, 'devices'])
    device_url = '/'.join([base_url, device_id])
    session = google.auth.transport.requests.AuthorizedSession(credentials)
    r = session.get(device_url)
    print(device_url, r.status_code)
    if r.status_code == 404:
        print('Registering....')
        r = session.post(base_url, data=json.dumps({
            'id': device_id,
            'model_id': device_model_id,
            'client_type': 'SDK_LIBRARY'
        }))
        if r.status_code != 200:
            raise Exception('failed to register device: ' + r.text)
        print('\rDevice registered.')

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--credentials', type=existing_file,
                        metavar='OAUTH2_CREDENTIALS_FILE',
                        default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'google-oauthlib-tool',
                            'credentials.json'
                        ),
                        help='Path to store and read OAuth2 credentials')
    parser.add_argument('--device_model_id', type=str,
                        metavar='DEVICE_MODEL_ID', required=True,
                        help='The device model ID registered with Google')
    parser.add_argument(
        '--project_id',
        type=str,
        metavar='PROJECT_ID',
        required=False,
        help='The project ID used to register device instances.')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s ' +
        Assistant.__version_str__())

    args = parser.parse_args()
    with open(args.credentials, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))

    with Assistant(credentials, args.device_model_id) as assistant:
        events = assistant.start()

        print('device_model_id:', args.device_model_id + '\n' +
              'device_id:', assistant.device_id + '\n')

        if args.project_id:
            register_device(args.project_id, credentials,
                            args.device_model_id, assistant.device_id)

        for event in events:
            process_event(event, assistant.device_id)


if __name__ == '__main__':
    main()