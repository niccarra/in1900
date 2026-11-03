import numpy as np
import matplotlib.pyplot as plt
import ODESolver

'''
Koden for SEIR0 er hentet fra 
https://github.com/sundnes/solving_odes_in_python/blob/21b2caa703f12d2cef6f0017c69d607bccfc5fc6/docs/src/chapter5/SEEIIR.py
'''
class SEIR0:
    def __init__(self, beta=0.33, r_ia=0.1,
                 r_e2=1.25, lmbda_1=0.33,
                 lmbda_2=0.5, p_a=0.4, mu=0.2):

        self.beta = beta
        self.r_ia = r_ia
        self.r_e2 = r_e2
        self.lmbda_1 = lmbda_1
        self.lmbda_2 = lmbda_2
        self.p_a = p_a
        self.mu = mu

    def __call__(self, t, u):
        beta = self.beta
        r_ia = self.r_ia
        r_e2 = self.r_e2
        lmbda_1 = self.lmbda_1
        lmbda_2 = self.lmbda_2
        p_a = self.p_a
        mu = self.mu

        S, E1, E2, I, Ia, R = u
        N = sum(u)
        dS = -beta * S * I / N - r_ia * beta * S * Ia / N \
            - r_e2 * beta * S * E2 / N
        dE1 = beta * S * I / N + r_ia * beta * S * Ia / N \
            + r_e2 * beta * S * E2 / N - lmbda_1 * E1
        dE2 = lmbda_1 * (1 - p_a) * E1 - lmbda_2 * E2
        dI = lmbda_2 * E2 - mu * I
        dIa = lmbda_1 * p_a * E1 - mu * Ia
        dR = mu * (I + Ia)
        return [dS, dE1, dE2, dI, dIa, dR]

# Problem 1.a
def test_SEIR0():
    model = SEIR0()
    t = 0
    u_test_1 = [1, 2, 3, 4, 5, 6]
    '''
    Forventede verdier for du_expected_n var beregnet ved hjelp av Google Sheets
    '''
    du_expected_1 = [
        -0.12964285714,
        -0.5303571429,
        -1.104,
        0.7,
        -0.736,
        1.8,
    ]

    u_test_2 = [1, 1, 1, 1, 1, 1]
    du_expected_2 = [
        -0.12925,
        -0.20075,
        -0.302,
        0.3,
        -0.068,
        0.4,
    ]

    deltas_1 = model(t, u_test_1)
    np.testing.assert_allclose(deltas_1, du_expected_1, rtol=1e-10)

    deltas_2 = model(t, u_test_2)
    np.testing.assert_allclose(deltas_2, du_expected_2, rtol=1e-10)

# Problem 1.b
def solve_SEIR( model, T, N, S_0, E2_0):
    U0 = [S_0, 0, E2_0, 0, 0, 0]
    # Vi følger forslaget fra oppgave og bruker Runge-Kutta 4 som ODE solver
    solver = ODESolver.RungeKutta4(model)
    solver.set_initial_condition(U0)
    t_span = (0, T)
    t, u = solver.solve(t_span, N)
    return t, u

def test_solve_SEIR():
    model = SEIR0()
    T = 100
    N = 200
    S_0 = 1000
    E2_0 = 10
    t, u = solve_SEIR(model, T, N, S_0, E2_0)
    # Assert that the total population remains constant over time
    np.testing.assert_allclose(sum(u[-1]), sum(u[0]), rtol=1e-10)

# Problem 1.c
def plot_SEIR(t, u): 
    S = u[:, 0]
    I = u[:, 3]
    Ia = u[:, 4]
    R = u[:, 5]
    plt.plot(t, S, label='S')
    plt.plot(t, I, label='I')
    plt.plot(t, Ia, label='Ia')
    plt.plot(t, R, label='R')
    plt.legend()
    plt.title('Solution of the SEIR model')
    plt.xlabel('Time (days)')
    plt.ylabel('Number in each category')
    
    plt.show()


# Problem 1.d
if __name__ == "__main__":
    test_SEIR0()
    test_solve_SEIR()
    model = SEIR0(beta=0.4)
    t, u = solve_SEIR(model, T=200, N=400, S_0=5.5e6, E2_0=100)
    plot_SEIR(t, u)
