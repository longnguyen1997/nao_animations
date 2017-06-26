'''
COMPATIBLE ONLY WITH 32-BIT PYTHON.
Takes messages generated from learning_gestures
and sends them to NAO over the ALAnimatedSpeech
module. NAO speaks each message with its annotated
behaviors.
'''

import pickle, time
from naoqi import ALProxy

def load_and_speak():
    messages = pickle.load(open('pickles/messages.pickle'))
    speech = ALProxy("ALAnimatedSpeech", "192.168.0.10", 9559)
    print '\nAMOUNT OF MESSAGES:', len(messages)
    for i in range(1, len(messages) + 1):
        print 'Message ' + str(i) + ': ' + messages[i - 1]
        speech.say(messages[i - 1])
        time.sleep(3) # Wait before speaking the next message.

# Run in command console.
load_and_speak()
