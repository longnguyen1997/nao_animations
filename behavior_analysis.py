'''
Various modular functions that depend on each other for
data processing, the data being NAO's joint sensor
measurements for motion analysis.
'''
from time import sleep, time
from naoqi import ALProxy
from motion_analyzer import NAOMotionDataAnalyzer as MA
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

JOINT_NAMES = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll',
            'LWristYaw', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll',
            'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll',
            'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'LHand', 'RHand']

# ------ D E V E L O P M E N T ------- #

def proxy(module, ip='127.0.0.1', port=9559):
    '''
    Establishes a proxy to the corresponding
    NAOqi module.

    :param module: Name of module. Must be a string.
    :return: A proxy to module, running on IP 127.0.0.1
             and port 9559.
    '''
    return ALProxy(module, ip, port)

# Start the proxies.
motion_proxy = proxy("ALMotion")
behavior_proxy = proxy("ALBehaviorManager")

behaviors = behavior_proxy.getInstalledBehaviors()[1:] # Ignore behavior_1 (Choregraphe).

# ------ F U N C T I O N S ------- #

def print_behaviors():
    '''
    Prints behaviors currently
    installed in NAO's system.
    '''
    i = 0
    for behavior in behaviors:
        print i, behavior
        i += 1

def split_reports(reports):
    # Split each report by new line delimiter,
    # also removing first two header lines.
    split = [report.split('\n')[2:] for report in reports]
    # Get rid of irrelevant lines in each report.
    for i in xrange(len(split)):
        for j in reversed(xrange(len(split[i]))):
            if 'Tasks' in split[i][j]:
                break
        split[i] = split[i][:j]
    # Split each line of each report into its data.
    split = [[line.split() for line in report] for report in split]
    # Make the data dictionary.
    angles = {body_part: [] for body_part in JOINT_NAMES}
    # Add the angles.
    for report in split:
        for line in report:
            angles[line[0]].append(float(line[2]))
    return angles

def process(data):
    reports = set()
    i = 1
    for b in data:
        print str(i) + ') ' + b
        behavior_proxy.post.runBehavior(b)
        sleep(0.1) # Wait 100ms for latency
        while behavior_proxy.isBehaviorRunning(b):
            reports.add(motion_proxy.getSummary())
    return split_reports(list(reports))

def dump_gesture_data(behaviors, name):
    '''
    Dumps gesture data into file name.

    :param behaviors: Behaviors to process and dump.
    :param name: Name of file to be saved.
    '''
    from pickle import dump
    dump(process(behaviors), open('pickles/gesture_data/' + name, 'wb'))

def time_series(behav, save_directory='plots/time_series/standing_bodytalk', return_data=False):
    '''
    Generates time series plots for all 26 of NAO's joints
    while they perform a specified behavior.

    :param behav: Behavior to be performed.
    :param save_directory: Directory to save plots in.
    '''

    def get_angles(data):
        '''
        Given a dataset, only find the radian angle
        corresponding to NAO's sensor movements.

        :param data: Data to sift through for get_angles.
        :return: An array of angles in float format.
        '''
        angles = []
        for i in xrange(len(data)):
            split = data[i].split('\n')[2:] # Remove first 2 header rows.
            cutoff = 0 # Find where to split the file.
            for j in range(len(split)):
                if 'Tasks' in split[j]:
                    cutoff = j; break
            angles.append([t[2] for t in [l.split() for l in split[:cutoff]]])
        return [[float(n) for n in report] for report in angles]

    # Allocate arrays for data collection.
    # Entries are time-sequential by index.
    data = []
    times = []

    behavior_proxy.runBehavior(behav)

    # Begin data collection as behavior runs.
    t = time()
    behavior_proxy.post.runBehavior(behav)
    sleep(0.125) # Account for latency.
    while behavior_proxy.isBehaviorRunning(behav):
        data.append(motion_proxy.getSummary())
        times.append(time() - t)

    # O(n) algorithm to filter by threshold-time intervals.
    keep = [0]
    threshold = 0.2
    begin = 0
    end = 0
    while end < len(times):
        if times[end] - times[begin] >= threshold:
            keep.append(end)
            begin = end
        else:
            end += 1

    # Postprocess the data.
    angles = get_angles(data)
    for n in reversed([t for t in range(len(times)) if t not in keep]):
        times.pop(n)
        angles.pop(n)

    print '\nNumber of data points:', len(angles), '\n'

    if return_data:
        return threshold, angles

    gesture = behav.split('/')[-1]  # Name of gesture without directory prefixes.

    # Plot the data, 26 colors, 26 joints.
    num_colors = 26
    ax = plt.subplot(111)
    cm = plt.get_cmap('jet')
    ax.set_color_cycle([cm(1. * i / num_colors) for i in range(num_colors)])
    for i in xrange(num_colors):
        ax.plot(times, [joint[i] for joint in angles], label=JOINT_NAMES[i], linewidth=0.7,
                path_effects=[path_effects.SimpleLineShadow(offset=(0.5, -0.5)), path_effects.Normal()])

    # Decorate the graph and save figure to .pdf format.
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.74, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1.06, 0.5), prop={'size': 7})
    plt.xlabel('Time after behavior initialization (s)')
    plt.ylabel('Joint angle (rad)')
    plt.title(gesture)
    plt.savefig(save_directory + '/' + gesture + '.pdf')
    plt.close()
