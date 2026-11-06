from SEIR import SEIR
from lockdown import Beta
import numpy as np

# Problem 5.a
class SEIRimport(SEIR):
    def __init__(self, beta=0.33, r_ia=0.1, r_e2=1.25, lmbda_1=0.33, lmbda_2=0.5, 
                 p_a=0.4, mu=0.2, sigma=0):
        super().__init__(beta, r_ia, r_e2, lmbda_1, lmbda_2, p_a, mu)
        self.sigma = sigma

    def __call__(self, t, u):
        dS, dE1, dE2, dI, dIa, dR = super().__call__(t, u)
        return [dS, dE1, dE2 + self.sigma, dI, dIa, dR]

# Problem 5.b
def test_SEIRimport():
    sigma = 10
    t = 0
    u = [1, 2, 3, 4, 5, 6,]

    model_1 = SEIR()
    model_2 = SEIRimport(sigma=sigma) 

    deltas_1 = model_1(t, u)
    deltas_2 = model_2(t, u)

    np.testing.assert_allclose(np.delete(deltas_1, 2), np.delete(deltas_2, 2), rtol=1e-10)
    np.testing.assert_allclose(deltas_1[2] + sigma, deltas_2[2])

if __name__ == "__main__":
    from SEIR import solve_SEIR, plot_SEIR
    test_SEIRimport()
    # Problem 5.c
    beta = Beta('r_values.txt')
    model = SEIRimport(beta, sigma=10)
    t, u = solve_SEIR(model, T=600, N=600, S_0=5.5e6, E2_0=100)
    plot_SEIR(t, u, components = ['I','Ia'])
