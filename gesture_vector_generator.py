import pickle
from time import sleep
from multiprocessing import Process
from sklearn.feature_extraction import DictVectorizer
from naoqi import ALProxy

ROBOT_IP = "192.168.0.10"
PORT = 9559

motion = ALProxy("ALMotion", ROBOT_IP, PORT)
behavior = ALProxy("ALBehaviorManager", ROBOT_IP, PORT)
animations = pickle.load(open('pickles/valid_gestures.pickle', 'rb'))
gesture_vectors = {g : [] for g in animations}

for gesture in animations:
    behavior_name = animations[gesture]
    # While gesture is running, keep adding data vectors.
    data = []
    behavior.post.runBehavior(behavior_name)
    # Induce 150ms delay to account for latency.
    sleep(0.15)
    while behavior.isBehaviorRunning(behavior_name):
        data.append(motion.getSummary())
    for report in data:
        try:
            # Each line looks like the following:
            # BODYPART STIFFNESS COMMAND SENSOR,
            # where the last 3 are numerics.
            lines = report.split('\n')[2:]
            lines = [' '.join(l.split()).split(' ') for l in lines][:-6]
            measurements = []
            for l in lines:
                measurements.append({'bodypart' : l[0], 'stiffness' : float(l[1]),
                                     'command' : float(l[2]), 'sensor' : float(l[3])})
            v = DictVectorizer()
            gesture_vectors[gesture].append(v.fit_transform(measurements).toarray())
        # Ignore this piece of data if it's broken.
        except:
            continue
    sleep(10) # Wait before going to the next animation.

for k in gesture_vectors: print len(gesture_vectors[k])
pickle.dump(gesture_vectors, open('pickles/gesture_feature_vectors.pickle', 'wb'))
