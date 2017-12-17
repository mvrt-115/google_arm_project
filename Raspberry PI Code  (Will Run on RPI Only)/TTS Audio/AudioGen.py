# Used to generate audio files from Google Assistant
import os
from pydub import AudioSegment
from gtts import gTTS

while True:
    textIn = input('Text to convert: ')
    textIn = 'repeat after me ' + textIn
    os.system('gtts-cli "' + str(textIn) + '" -o temp.mp3')
    sound = AudioSegment.from_mp3("temp.mp3")
    sound.export("temp.wav", format="wav")
    fileName = input('Output file name: ')
    os.system('googlesamples-assistant-pushtotalk -i temp.wav -o ' + fileName)
