from time import sleep, time
from naoqi import ALProxy
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import numpy as np


# ------ D E V E L O P M E N T ------- #

def proxy(module):
    '''
    Establishes a proxy to the corresponding
    NAOqi module.

    :param module: Name of module. Must be a string.
    :return: A proxy to module, running on IP 127.0.0.1
             and port 9559.
    '''
    return ALProxy(module, '127.0.0.1', 9559)

# Start the proxies.
motion = proxy("ALMotion")
behavior = proxy("ALBehaviorManager")

behaviors = behavior.getInstalledBehaviors()[2:]
behaviors = [b for b in behaviors if
             'Loop' not in b and 'Exhausted_2' not in b and 'Excited_1' not in b]  # remove loops

# ------ F U N C T I O N S ------- #

def split_reports(reports):
    # Split each report by new line delimiter.
    split = [report.split('\n') for report in reports]
    # Get rid of irrelevant lines in each report.
    for i in xrange(len(split)):
        for j in xrange(len(split[i])):
            if 'Tasks' in split[i][j]:
                break
        split[i] = split[i][:j]
    # Get rid of header lines in each report.
    split = [report[2:] for report in split]
    # Split each line of each report into its data.
    split = [[line.split() for line in report] for report in split]
    # Make the data dictionary.
    angles = {body_part: [] for body_part in motion.getBodyNames('Body')}
    # Add the angles.
    for report in split:
        for line in report:
            angles[line[0]].append(float(line[2]))
    return angles

def process(data):
    reports = set()
    for b in data:
        print b
        behavior.post.runBehavior(b)
        sleep(0.1)
        while behavior.isBehaviorRunning(b):
            reports.add(motion.getSummary())
    return split_reports(list(reports))

def body_data():
    '''
    Return a visual representation of
    NAO's current joint sensor data.

    :return: Report of NAO's sensors and their angles.
    '''
    return motion.getSummary()

def dump_gesture_data(obj, name):
    '''
    Dumps gesture data into file name.

    :param obj: Data to dump. MUST be in proper format.
    :param name: Name of file to be saved.
    '''
    from pickle import dump
    dump(obj, open('pickles/gesture_data/' + name, 'wb'))

def extract_command(line):
    '''
    Extracts an angle command from a given line.

    :param line: Line to extract from. Must be derived
                 from NAO's joint sensor reports.
    '''
    return [float(s) for s in line.split()[2:][::4][1:]]

def time_series(behav, save_directory='plots/time_series/standing_bodytalk', return_data=False):
    '''
    Generates time series plots for all 26 of NAO's joints
    while they perform a specified behavior.

    :param behav: Behavior to be performed.
    :param save_directory: Directory to save plots in.
    '''

    def get_only_angles(data):
        '''
        Given a dataset, only find the radian angles
        corresponding to NAO's sensor movements.

        :param data: Data to sift through for angles.
        :return: An array of angles in float format.
        '''
        out = []
        for i in xrange(len(data)):
            split = data[i].split('\n')[2:] # Remove first 2 header rows.
            cutoff = 0 # Find where to split the file.
            for j in range(len(split)):
                if 'Tasks' in split[j]:
                    cutoff = j; break
            out.append([t[2] for t in [l.split() for l in split[:cutoff]]])
        return [[float(n) for n in report] for report in out]

    # Allocate arrays for data collection.
    # Entries are time-sequential by index.
    data = []
    times = []

    # Begin data collection as behavior runs.
    t = time()
    behavior.post.runBehavior(behav)
    sleep(0.125) # Account for latency.
    while behavior.isBehaviorRunning(behav):
        data.append(motion.getSummary())
        times.append(time() - t)

    # O(n) algorithm to filter by 0.15s intervals.
    keep = [0]
    begin = 0
    end = 0
    while end < len(times):
        if times[end] - times[begin] >= 0.15:
            keep.append(end)
            begin = end
        else:
            end += 1

    # Postprocess the data.
    nums = get_only_angles(data)
    for n in reversed([t for t in range(len(times)) if t not in keep]):
        times.pop(n)
        nums.pop(n)

    print '\nNumber of data points:', len(nums), '\n'

    if return_data:
        return np.array(times), np.array(nums)

    gesture = behav.split('/')[-1]  # Name of gesture without directory prefixes.

    # Plot the data, 26 colors, 26 joints.
    num_colors = 26
    ax = plt.subplot(111)
    cm = plt.get_cmap('jet')
    ax.set_color_cycle([cm(1. * i / num_colors) for i in range(num_colors)])
    names = motion.getBodyNames('Body')
    for i in xrange(num_colors):
        ax.plot(times, [joint[i] for joint in nums], label=names[i], linewidth=0.7,
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

data = time_series(behaviors[10], return_data=True)