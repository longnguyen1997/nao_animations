'''
COMPATIBLE ONLY WITH 32-BIT PYTHON.
Takes messages generated from learning_gestures
and sends them to NAO over the ALAnimatedSpeech
module. NAO speaks each message with its annotated
behaviors.
'''

import pickle, time
from multiprocessing import Process
from naoqi import ALProxy

def load_and_speak(ROBOT_IP = "192.168.0.10", PORT = 9559):

    '''
    Loads messages processed from the user and prompts
    NAO to speak. Time analytics provided at runtime,
    detailing how long each message takes to say. Gestures
    are run in disabled body language mode.

    :param ROBOT_IP: NAO's current IP, default of 192.168.0.10.
    :param PORT: Hosting port for NAO's interface, default of 9559.
    :return: void
    '''

    messages = pickle.load(open('pickles/messages.pickle'))
    speech = ALProxy("ALAnimatedSpeech", ROBOT_IP, PORT)
    configuration = {"bodyLanguageMode" : "disabled"}
    delay = 2 # Delay in seconds.
    print '\nAMOUNT OF MESSAGES:', len(messages), '\n'
    for i in range(len(messages)):
        print '> MESSAGE ' + str(i + 1) + ':\n' + messages[i]
        start = time.time()
        speech.say(messages[i], configuration)
        total_time = time.time() - start
        print '    Message', i + 1, 'took', total_time, 'seconds to say.\n'
        time.sleep(delay) # Wait before saying next message.

# Run in command console.
load_and_speak()
