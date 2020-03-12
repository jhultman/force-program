import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle


class Animator:

    def __init__(self, pos, vel, force):
        self.pos = pos
        self.vel = vel
        self.force = force
        self.pos_interp = interpolate_pos(pos)
        self.fig, self.ax = plt.subplots(nrows=4, sharex=True, figsize=(9, 8))

    def init_lims(self):
        xmin, xmax = np.min(self.pos), np.max(self.pos)
        ymin, ymax = 0, 0.1
        border = 0.1 * (xmax - xmin)
        for a in self.ax:
            a.set(xlim=[xmin - border, xmax + border])

    def init_ticks(self):
        x0, x1 = self.pos[0], self.pos[-1]
        self.ax[3].set(yticks=[])

    def init_marker_lines(self):
        for x in self.pos[[0, -1]]:
            self.ax[3].axvline(x=x, color='grey', linestyle='dashed', alpha=0.5)

    def init_patch(self):
        self.patch = Rectangle((self.pos[0], 0), 0.05, 1, color='royalblue')
        self.ax[3].add_patch(self.patch)

    def init_ani(self):
        self.init_lims()
        self.init_ticks()
        self.init_marker_lines()
        self.init_patch()
        return self.patch,

    def step_ani(self, frame):
        self.patch.set_xy([self.pos_interp[frame], 0])
        return self.patch,

    def ani(self, fname):
        animation = FuncAnimation(
            self.fig,
            self.step_ani,
            frames=range(len(self.pos_interp)),
            init_func=self.init_ani,
            blit=True,
            interval=50,
            repeat=False,
        )
        animation.save(
            f'../images/{fname}.gif',
            writer='imagemagick',
            dpi=80,
        )

    def plot(self):
        T = len(self.pos)
        t = np.arange(T) / (T - 1)
        self.ax[0].plot(t, self.pos, c='royalblue')
        self.ax[1].plot(t, self.vel, c='orangered')
        self.ax[2].step(t, self.force, c='forestgreen')
        titles = ['pos', 'vel', 'force', 'traj']
        ylabels = ['(m)', '(m/s)', '(N)', '']
        for a, title, ylab in zip(self.ax, titles, ylabels):
            a.set(title=title, ylabel=ylab, xticklabels=[], xticks=t)


def interpolate_pos(pos, npoints=100):
    numel = len(pos)
    t = np.linspace(0, numel, npoints)
    pos = np.interp(t, range(numel), pos)
    return pos


def plot_and_animate(pos, vel, force, fname):
    animator = Animator(pos, vel, force)
    animator.plot()
    animator.ani(fname)


if __name__ == '__main__':
    main()
