# -*- encoding: UTF-8 -*-

import sys
import time

from naoqi import ALProxy, ALBroker, ALModule
from optparse import OptionParser
from pickle import load

NAO_IP = "nao.local"

# Global variable storing the module instance.
NAOInteraction = None


class SpeechGestures(ALModule):

    def __init__(self, name):
        ALModule.__init__(self, name)
        self.tts = ALProxy("ALTextToSpeech")
        self.mp = ALProxy("ALMotion")
        self.bp = ALProxy("ALBehaviorManager")


def main():
    parser = OptionParser()
    parser.add_option("--pip", help="NAO's IP address.", dest="pip")
    parser.add_option("--pport",
                      help="Parent broker port. The port NAOqi listens on.",
                      dest="pport",
                      type="int")
    parser.set_defaults(pip=NAO_IP, pport=9559)
    (opts, args_) = parser.parse_args()
    pip = opts.pip
    pport = opts.pport

    # Broker used to construct NAOqi modules and subscribe to other modules.
    # Broker is active until the program terminates.
    myBroker = ALBroker("myBroker",
                        "0.0.0.0",  # Listen to anyone.
                        0,         # Use any free port.
                        pip,       # Parent broker IP address.
                        pport)     # Parent broker port.

    global NAOInteraction
    NAOInteraction = HumanGreeterModule("NAOInteraction")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "INTERRUPTED: Shutting down speech module now."
        myBroker.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()
