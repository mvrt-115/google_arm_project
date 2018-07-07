################################################
#           __  ___ _   __ ___  ______         #
#          /  |/  /| | / // _ \/_  __/         #
#         / /|_/ / | |/ // , _/ / /            #
#        /_/  /_/  |___//_/|_| /_/             #
#                                              #
################################################

# Class: main.py
# Description: Handles the game logic and user interaction using the Assistant SDK.

# Project: MVRTxGoogle Robotic Arm
# Project Descripton:
# 2018 Monta Vista Robotics Team, Cupertino, CA

##main.py inherited from GoogleCAHotword.py

from __future__ import print_function

import argparse
import os.path
import json

import google.auth.transport.requests
import google.oauth2.credentials

import time

from Arm import Arm
from TTT import TTTGame
from GRQD import GRQDGame
from pygame import mixer

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file

arm = Arm("/dev/ttyACM0", False) #Creates Arm object
time.sleep(5) #Sleeps for 5 seconds to verify start
arm.aWrite("N") #Sends the start serial command

ttt = TTTGame(arm)
grqd = GRQDGame(arm)
guesses = 4
game = "none" #Variable to hold type of game being played.


# Function: play_audio(toSay);
# Takes string "toSay" and parses with Google Cloud Text-to-Speech API and provides
# spoken result of string. FUNCTIONALITY TO BE IMPLEMENTED.
def play_audio(toSay):
    #Function to control TextToSpeech (using new Google Cloud Text-to-Speech API)
    print(toSay)

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
    global game
    global ttt
    global arm
    global grqd
    global guesses

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
                    ttt.board.board = [0]*10
                    game = "ttt"

                    ttt.drawBoard()
                    play_audio("Would you like to be X or O?")
                    ttt.board.draw()
                elif gameIn == "RGQD":
                    game = "rgqd"
                    grqd.chooseObjects()
                    grqd.generateCoordinates()

                    grqd.drawObject(grqd.xCoords, grqd.yCoords)
                    play_audio("This game reverses the role of Google Quick Draw.")
                    play_audio("You have 4 guesses to choose what the object is:")
                    play_audio("a " + grqd.choices[0] + ", a " + grqd.choices[1] + ", a " + grqd.choices[2] + ", or a " + grqd.choices[3] + ".")

            if command == "com.acme.commands.set_letter":
                letter = params["letter"]
                if game == "ttt":
                    if letter == "X":
                        ttt.setPLetter(1)
                    elif letter == "O":
                        ttt.setPLetter(2)
                    ttt.board.draw()


            if command == "com.acme.actions.choose_position":
                pos = int(params['position'])
                print(pos)
                if game == "ttt":
                    print('moving')
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
                            play_audio("You have " + str(guesses) + " guesses left.")
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
