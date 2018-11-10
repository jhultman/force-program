import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt
from animator import animate_solution


def lower_triangular_ones(N):
    A = np.zeros((N, N))
    inds = np.tril_indices_from(A)
    A[inds] = 1
    return A


def build_vel_pos_matrices(N, mass):
    A_vf = 1 / mass * lower_triangular_ones(N)
    A_xv = lower_triangular_ones(N)

    rng = np.arange(N)
    A_xv[rng, rng] = 1 / 2

    A_xf = A_xv @ A_vf
    return A_xf, A_vf


def build_state_matrix(A_xf, A_vf):
    a_xf = A_xf[-1, :]
    a_vf = A_vf[-1, :]
    A = np.vstack((a_xf, a_vf))
    return A


def solve_force_program_analytically(A, y_d):
    f = A.T @ np.linalg.inv(A @ A.T) @ y_d
    return f


def solve_force_program_cvxpy(N, A, y_d, norm=2):
    f = cp.Variable(N)
    y_d = np.array([1, 0])

    constraints = [(A @ f) == y_d]
    J = cp.norm(f, p=norm)
    obj = cp.Minimize(J)
    cp.Problem(obj, constraints).solve()
    return f.value


def construct_x_v(f, A_xf, A_vf):
    x = A_xf @ f
    v = A_vf @ f
    return x, v


def prep_xvf_for_plot(x, v, f):
    to_concat = ([0], x, [0], v, f[:1], f)
    pos, vel, force = np.concatenate(to_concat).reshape(3, -1)
    return pos, vel, force


def plot_experiment(pos, vel, force, fname='mass'):
    fig, ax = plt.subplots(nrows=3, sharex=True)
    titles = ['pos', 'vel', 'force']
    ylabels = ['(m)', '(m/s)', '(N)']
    xlabels = ['', '', '(s)']
    t = range(len(pos))

    ax[0].plot(pos, c='blue')
    ax[1].plot(vel, c='red')
    ax[2].step(t, force, c='green')

    for a, t, xlab, ylab in zip(ax, titles, xlabels, ylabels):
        a.set_title(t)
        a.set_xlabel(xlab)
        a.set_ylabel(ylab)

    fig.tight_layout()
    plt.savefig(f'../images/{fname}.png')


def interpolate(pos):
    numel = len(pos)
    t = np.linspace(0, numel, 500)
    pos = np.interp(t, range(numel), pos)
    return pos


def main():
    N, mass = 10, 1
    y_d = np.array([1, 0])

    A_xf, A_vf = build_vel_pos_matrices(N, mass)
    A = build_state_matrix(A_xf, A_vf)

    for norm in [1, 2, 'inf']:
        f = solve_force_program_cvxpy(N, A, y_d, norm)
        x, v = construct_x_v(f, A_xf, A_vf)
        pos, vel, force = prep_xvf_for_plot(x, v, f)

        plot_experiment(pos, vel, force, fname=f'l_{norm}')
        animate_solution(pos, fname=f'l_{norm}_ani')


if __name__ == '__main__':
    main()
