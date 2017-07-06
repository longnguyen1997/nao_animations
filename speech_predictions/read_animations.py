'''
This module takes in the NAO animations provided
by Aldebaran, parsing them into usable dictionary
and list objects that depend on each other.
This information is used in other modules that
require learning and adaptive string formulation
for NAO behavior.
'''

folder = '../animation_info/'

# Get animation dictionary for full-name reference.
with open(folder + 'nao_animations.csv') as f:
    animations = f.readlines()[1:]
animations = [tuple(a.split(',')[:-1]) for a in animations]
# Dictionary of gestures and their full names,
# where keys are gesture names and values are NAO directory references.
animations_dict = {t[0]:t[1] for t in animations}

# Get animations keyed by tags.
with open(folder + 'nao_animations_tagged.csv') as f:
    # Omit the first row, which contains the column headers.
    tagged_animations = f.readlines()[1:]
# Break lines into tags and their corresponding gestures.
tagged_animations = [a.split(',') for a in tagged_animations]
animations_by_tag = {a[0]:[w.strip() for w in a[1].split(';')] for a in tagged_animations}

# Get grouped tags for later machine learning.
# 9 classes to learn:
# 'good', 'uncertain', 'self', 'disagree',
# 'greeting', 'tell', 'other', 'ask', 'agree'
with open(folder + 'grouped_tags.csv', 'rU') as f:
    lines = f.readlines()[1:]
    lines = [l.strip().split(',') for l in lines]
grouped_tags = {group:[] for group in [l[1] for l in lines]}
for l in lines:
    grouped_tags[l[1]].append(l[0])

def run(animation):
    '''
    Suspend the speech, run an animation and resume the speech.
    :param animation: Animation to be referenced.
    :return: String representation of NAO command.
    '''
    return "^run(" + animation + ")"

def start(animation):
    '''
    Start an animation.
    :param animation: Animation to be referenced.
    :return: String representation of NAO command.
    '''
    return "^start(" + animation + ")"

def stop(animation):
    '''
    Stop an animation.
    :param animation: Animation to be referenced.
    :return: String representation of NAO command.
    '''
    return "^stop(" + animation + ")"

def wait(animation):
    '''
    Suspend the speech, wait for the end of
    the animation and resume the speech.
    :param animation: Animation to be referenced.
    :return: String representation of NAO command.
    '''
    return "^wait(" + animation + ")"
