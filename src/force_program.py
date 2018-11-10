import numpy as np
import cvxpy as cp
import numpy.linalg as la
import matplotlib.pyplot as plt
from animator import plot_and_animate


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
    mats = (A.T, la.inv(A @ A.T), y_d)
    f = la.multi_dot(mats)
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
    vals = ([0], x, [0], v, f[:1], f)
    pos, vel, force = np.concatenate(vals).reshape(3, -1)
    return pos, vel, force


def main():
    N, mass = 10, 1
    y_d = np.array([1, 0])

    A_xf, A_vf = build_vel_pos_matrices(N, mass)
    A = build_state_matrix(A_xf, A_vf)

    for norm in [1, 2, 'inf']:
        f = solve_force_program_cvxpy(N, A, y_d, norm)
        x, v = construct_x_v(f, A_xf, A_vf)
        pos, vel, force = prep_xvf_for_plot(x, v, f)
        plot_and_animate(pos, vel, force, fname=f'l_{norm}')


if __name__ == '__main__':
    main()
