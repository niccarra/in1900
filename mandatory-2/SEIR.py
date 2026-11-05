from re import match

import numpy as np
import matplotlib.pyplot as plt
from SEIR0 import SEIR0, solve_SEIR

# Problem 2.a
class SEIR(SEIR0):
    def __init__(self, beta=0.33, r_ia=0.1,
                 r_e2=1.25, lmbda_1=0.33, lmbda_2=0.5,
                 p_a=0.4, mu=0.2):

        if isinstance(beta, (float, int)): # is it a number?
            self.beta_function = lambda t: beta # wrap as a function
        elif callable(beta): # is it a function?
            self.beta_function = beta
        else:
            raise TypeError("beta must be a number or a function")
        
        super().__init__(self.beta_function(0), r_ia, r_e2, lmbda_1, lmbda_2, p_a, mu)

    def __call__(self, t, u):
        self.beta = self.beta_function(t)
        return super().__call__(t, u)

# Problem 2.b
def test_SEIR_beta_const():
    '''
    En kopi av test_SEIR0() fra SEIR0.py
    '''
    model = SEIR()

    t = 0
    u_test_1 = [1, 2, 3, 4, 5, 6]

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

def test_SEIR_beta_var():
    model = SEIR(beta=lambda t: 0.33 - 0.0033 * t)
    
    u_test = [1, 2, 3, 4, 5, 6]

    # forventede verdier for t = 30
    du_expected_t30 = [
        -0.09075,
        -0.56925,
        -1.104,
        0.7,
        -0.736,
        1.8,
    ]

    # forventede verdier for t = 60
    du_expected_t60 = [
        -0.051857142857,
        -0.6081428571,
        -1.104,
        0.7,
        -0.736,
        1.8,
    ]
    
    deltas_t30 = model(t = 30, u = u_test)
    np.testing.assert_allclose(deltas_t30, du_expected_t30, rtol=1e-10)

    deltas_t60 = model(t = 60, u = u_test)
    np.testing.assert_allclose(deltas_t60, du_expected_t60, rtol=1e-10) 

# Problem 2.c
def plot_SEIR(t, u, components=['S','I', 'Ia', 'R']):
    for comp in components:

        # Kartlegg komponentnavn til indeksen i u
        match comp:
            case 'S':
                i = 0
            case 'E1':
                i = 1
            case 'E2':
                i = 2
            case 'I':
                i = 3
            case 'Ia':
                i = 4
            case 'R':
                i = 5
            case _:
                i = None
                print(f"Warning: Component '{comp}' not recognized. Skipping.")  

        if i is not None:
            plt.plot(t, u[:, i], label=comp)
    
    plt.legend()
    plt.title('Solution of the SEIR model')
    plt.xlabel('Time (days)')
    plt.ylabel('Number in each category')
    
    plt.show()

if __name__ == "__main__":
    test_SEIR_beta_const()    
    test_SEIR_beta_var()

    model = SEIR(beta= 0.4)
    t, u = solve_SEIR(model, T = 200, N = 400, S_0 = 5.5e6, E2_0 = 100)
    plot_SEIR(t, u)

    #Problem 2.d
    '''
    La oss finne t som maksimiserer I(t). Vi er interesserte kun i I fordi Ia representerer asymptomatiske 
    individuer som ikke trenger behandling.
    '''

    I = u[:, 3]
    print(f"Maximalt antall syke individer: {np.ceil(max(I))}") # Skriver ut 258544.0
    '''
    Ifølge oppgaven 20% av de smittede vil trenge behandling, og 25% av de som trenger behandling vil trenge 
    mekanisk ventilasjon. Altså 258544 * 0.2 * 0.25 = 12927.2 individer vil trenge mekanisk ventilasjon på det meste.
    Siden det er kun 700 mekaniske ventilatorer tilgjengelig, vil det være et stort overbelastning på sykehusene.
    Omtrent 1 av 18 individer som trenger mekanisk ventilasjon vil få det, ellers circa 5% av de med behov for mekanisk ventilasjon.
    '''