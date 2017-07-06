from time import sleep
from naoqi import ALProxy

def proxy(module):
    return ALProxy(module,'127.0.0.1',9559)

def split_reports(reports):
    # Split each report by new line delimiter.
    split = [report.split('\n') for report in reports]
    # Get rid of irrelevant lines in each report.
    for i in range(len(split)):
        for j in range(len(split[i])):
            if 'Tasks' in split[i][j]:
                break
        split[i] = split[i][:j]
    # Get rid of header lines in each report.
    split = [report[2:] for report in split]
    # Split each line of each report into its data.
    split = [[line.split() for line in report] for report in split]
    # Make the data dictionary.
    angles = {body_part : [] for body_part in motion.getBodyNames('Body')}
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
    print motion.getSummary()

motion = proxy("ALMotion")
behavior = proxy("ALBehaviorManager")

behaviors = behavior.getInstalledBehaviors()[2:]
behaviors = [b for b in behaviors if 'Loop' not in b] # remove loops

def extract_command(line):
    return [float(s) for s in line.split()[2:][::4][1:]]

negative_emotions = [r for r in behaviors if 'Emotions/Negative' in r]
negative_data = process(negative_emotions)
