class NAOMotionDataAnalyzer():
    '''
    Motion analysis and functional movement module. Takes given data in
    proper format (a dictionary of the 26 different sensors on NAO's body
    whose values are all measurements taken of each sensor) belonging
    to a certain category of movements.

    Supports plotting movement distribution, and NAO can be controlled to
    generate new, natural movements based on statistical sampling from
    the data given.
    '''

    def __init__(self, filename, robot_ip='127.0.0.1'):
        '''
        Start a new instance of the motion analytics module. A NAO instance (whether
        simulated or physical) MUST be running when creating this module.

        :param filename: The name of the data file. May also include subdirectories.
        :param robot_ip: NAO's IP, in string format. Defaulted to 127.0.0.1 (Webots simulation).
        '''
        from naoqi import ALProxy
        from pickle import load
        from numpy import std, mean

        self.file = filename
        self.ip = robot_ip
        self.data = load(open(filename, 'rb'))
        self.means_stds = {k: (mean(self.data[k]), std(self.data[k]))
                           for k in self.data}
        self.data_bounds = {k : (self.means_stds[k][0]-self.means_stds[k][1], self.means_stds[k][0]+self.means_stds[k][1])
                            for k in self.means_stds}
        self.motion_proxy = ALProxy("ALMotion", robot_ip, 9559)
        self.motion_proxy.wakeUp()

    def __str__(self):
        return 'CURRENTLY WORKING WITH DATA FILE: ' + self.file + '\nNAO\'S IP ADDRESS: ' + self.ip

    def plot_distribution(self, save_directory, rug=False):
        '''
        Using a kernel density estimate, plots sensor reading
        frequencies from the data given. Saves these 26 plots
        to save_directory.

        :param save_directory: Directory to save plots in.
        :param rug: Whether or not to show a rug (color indicator)
                    at the bottom of the plots. Takes significantly more time.
        '''
        import matplotlib.pyplot as plt
        import seaborn as sns
        from pylab import rcParams
        from matplotlib import rc

        rcParams['figure.figsize'] = 5.5, 3.8
        for k in self.data.keys():
            sns.distplot(self.data[k], hist=False, rug=rug)
            plt.title(k + ' Sensor Distribution', fontdict={'fontsize': 14}, style='italic')
            plt.xlabel("Angle (rad)")
            plt.ylabel("Frequency")
            plt.savefig(save_directory + '/' + k + '.pdf', bbox_inches='tight')
            plt.clf()

    def generate_motion(self):
        '''
        Generates new motion data given the data this module is working with.

        :return: Randomly generated data for each of the 26 NAO sensors
                 that is statistically within the means of the dataset by its
                 respective standard deviations.
        '''
        from random import uniform
        return {k: uniform(self.data_bounds[k][0], self.data_bounds[k][1]) for k in self.data_bounds}

    def move_nao(self, time):
        '''
        Generates new motion data and interpolates (moves) NAO
        accordingly. All 26 joints are moved at the same time.

        :param time: How long the animation should last.
        '''
        data = self.generate_motion()
        names = data.keys()
        angles = data.values()
        self.motion_proxy.angleInterpolation(names, angles, time, True)
