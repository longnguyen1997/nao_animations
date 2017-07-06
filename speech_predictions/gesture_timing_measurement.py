from naoqi import ALProxy as Proxy
from read_animations import animations_dict, run
from time import sleep
from time import time

def proxy(module):
    return Proxy(module, "192.168.0.10", 9559)

speech = proxy("ALAnimatedSpeech")
behavior = proxy("ALBehaviorManager")

gesture_times = {g : 0 for g in animations_dict.keys()}
configuration = {"bodyLanguageMode" : "disabled"}

for gesture in animations_dict.keys():
    # ------MEASURING GESTURE TIME...------
    start = time()
    speech.say(run(gesture), configuration)
    elapsed = time() - start
    # ------------------------------------
    gesture_times[gesture] += elapsed
    sleep(15) # Delay before moving on.
