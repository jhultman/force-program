import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle


class Animator:

    def __init__(self, x):
        self.x = x
        self.fig, self.ax = plt.subplots(figsize=(10, 2))
        self.fig.tight_layout()

    def init_lims(self):
        xmin, xmax = np.min(self.x), np.max(self.x)
        ymin, ymax = 0, 0.1
        border = 0.1 * (xmax - xmin)
        self.ax.set_xlim(xmin - border, xmax + border)
        self.ax.set_ylim(ymin, ymax)

    def init_ticks(self):
        x0, x1 = self.x[0], self.x[-1]
        self.ax.set_xticks(np.linspace(x0, x1, 3))
        self.ax.set_yticks([])

    def init_marker_lines(self):
        for x in self.x[[0, -1]]:
            self.ax.axvline(x=x, color='grey', linestyle='dashed')

    def init_patch(self):
        self.patch = Rectangle((self.x[0], 0), 0.1, 0.1, color='skyblue')
        self.ax.add_patch(self.patch)

    def init_ani(self):
        self.init_lims()
        self.init_ticks()
        self.init_marker_lines()
        self.init_patch()
        return self.patch,

    def step_ani(self, frame):
        self.patch.set_xy([self.x[frame], 0])
        return self.patch,

    def ani(self, fname):
        args = ()
        animation = FuncAnimation(
            self.fig, 
            self.step_ani, 
            frames=range(len(self.x)),
            init_func=self.init_ani, 
            blit=True, 
            interval=50,
            repeat=False,
        )
        animation.save(f'../images/{fname}.gif', dpi=80, writer='imagemagick')


def interpolate(pos):
    numel = len(pos)
    t = np.linspace(0, numel, 100)
    pos = np.interp(t, range(numel), pos)
    return pos


def animate_solution(pos, fname='mass'):
    pos = interpolate(pos) 
    animator = Animator(pos)
    animator.ani(fname)
