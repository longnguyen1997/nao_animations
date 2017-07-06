class NAOMotionDataAnalyzer():
    def __init__(self, filename, robot_ip):
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
        import matplotlib.pyplot as plt
        import seaborn as sns
        from pylab import rcParams
        from matplotlib import rc

        # rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
        # rcParams['text.usetex'] = True
        # rcParams['text.latex.preamble'] = [r'\usepackage{lmodern}']
        rcParams['figure.figsize'] = 5.5, 3.8
        for k in self.data.keys():
            sns.distplot(self.data[k], hist=False, rug=rug)
            plt.title(k + ' Sensor Distribution', fontdict={'fontsize': 14}, style='italic')
            plt.xlabel("Angle (rad)")
            plt.ylabel("Frequency")
            plt.savefig(save_directory + '/' + k + '.pdf', bbox_inches='tight')
            plt.clf()

    def generate_motion(self):
        from random import uniform
        return {k: uniform(self.data_bounds[k][0], self.data_bounds[k][1]) for k in self.data_bounds}

    def move_nao(self, time):
        data = self.generate_motion()
        names = data.keys()
        angles = data.values()
        self.motion_proxy.angleInterpolation(names, angles, time, True)
