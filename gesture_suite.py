from os import listdir
from pickle import load


class GestureModule():
    """
    A module responsible for one certain type
    of gesture, such as "yes", "no", "happy", etc.

    Relies on stochastic data generation based
    on data given, interpolated over a given interval
    of time.
    """

    def __init__(self, analyzer, time):
        """
        Creates an instance of the gesture module.

        @param analyzer: A NAOMotionDataAnalyzer
                         instance containing the data
                         and statistics for the gesture type.
        @param time: How long each generated movement should last.
        """
        self.analyzer = analyzer
        self.time = time

    def move(self, total_time):
        for i in range(int(total_time / self.time)):
            self.analyzer.move(self.time)

    def wake_up(self):
        self.analyzer.reestablish_connection()


class GestureSuite():
    """
    A suite for all of NAO's generated
    gesture modules. Loads in all modules
    it can find under the directory provided.

    Operates jointly with speech modules that pass
    in a queue of types of gestures to perform with
    their animation times.
    """

    def __init__(self, directory='pickles/gesture_data/'):
        """
        Initializes the class.
        Wakes up all the modules loaded to
        ensure connection with NAO.

        @param directory: Relative path to search in
                          for modules. Defaulted to
                          'pickles/gesture_data/'.
        """
        self.modules = {}
        for filename in listdir(directory):
            try:
                self.modules[filename] = load(open(filename), 'rb')
            except:
                print 'Invalid file. Check your directory again.'
                return
        # Print a warning if no modules were found.
        if not self.modules:
            print 'WARNING: You either have no modules or the directory is empty.'
        for module in self.modules.values():
            module.wake_up()

    def move(self, queue):
        """
        Moves NAO sequentially (hence the queue)
        according to category and time provided.

        @param queue: Queue of motions to direct NAO.
                      Must be a list of tuples [t_0, ..., t_n],
                      where t_i = (String category_i,
                                   float time_of_animation_i).
        """
        for pair in queue:
            category = pair[0]
            period = pair[1]
            if category in self.modules:
                self.modules[category].move(period)
