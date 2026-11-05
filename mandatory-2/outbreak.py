import numpy as np
from tabulate import tabulate
from SEIR import SEIR, solve_SEIR, plot_SEIR

# Problem 3.a
def R_to_beta(R, r_ia=0.1, r_e2=1.25, lmbda_2=0.5, p_a=0.4, mu=0.2):
   return R * np.pow((1 - p_a) * (r_e2 / lmbda_2 + 1 / mu) + p_a * r_ia / mu, -1) 

def test_R_to_beta():
   # Ifølge oppgaven, med default parameterverdier er R = 4.7 * beta
   R = 4.7
   beta = R_to_beta(R)
   np.testing.assert_allclose(beta, 1)

# problem 3.b
class LockdownBeta:
   def __init__(self, t_lock, beta_0, beta_1):
      self.beta_0 = beta_0
      self.beta_1 = beta_1
      self.t_lock = t_lock

   def __call__(self, t):
      if t < self.t_lock:
         return self.beta_0
      else:
         return self.beta_1

if __name__ == "__main__":
   test_R_to_beta()
   beta_0 = R_to_beta(3.2)
   beta_1 = R_to_beta(0.5)
   beta = LockdownBeta(t_lock=26, beta_0=beta_0, beta_1=beta_1)

   model = SEIR(beta=beta)
   t, u = solve_SEIR(model, T = 200, N = 400, S_0 = 5.5e6, E2_0 = 100)
   plot_SEIR(t, u, components=['I', 'Ia'])

   # Problem 3.c
   '''
   Utforske effekten av å endre tidspunktet for lockdown (t_lock) på tall av smittede.
   '''
   t_lockdowns =  [19, 26, 33, 40]
   betas = [LockdownBeta(t_lock, beta_0, beta_1) for t_lock in t_lockdowns]
   models = [SEIR(beta=beta) for beta in betas]
   results = [solve_SEIR(model, T = 200, N = 400, S_0 = 5.5e6, E2_0 = 100) for model in models]
   t = [result[0] for result in results]   
   u = [result[1] for result in results]
   max_i = [max(u_i[:, 3]) for u_i in u]
   n_ventilator = [i * 0.2 * 0.25 for i in max_i] # 20% av smittede trenger sykehus, 25% av disse trenger ventilator
   # Problem 3.d
   table = tabulate(zip(t_lockdowns, n_ventilator), headers=['Tidspunkt for lockdown (dager)', 'Antall ventilatorer'])
   print(table)
   '''
   Skriver ut
    Tidspunkt for lockdown (dager)    Antall ventilatorer
--------------------------------  ---------------------
                              19                103.798
                              26                387.512
                              33               1422.61
                              40               4916.88

   Vi kan se at det å vente en selv en uke mer for å innføre lockdown mer en 
   tredoblerer nummeret av ventilatorer som trengs. Og dette nummeret er mer en 
   dobelt av antall ventilatorer som var tilgjengelig i Norge. 
   
   Vi kunne også prøve å finne t_lockdown slik at antallet ventilatorer er likt 700

    Tidspunkt for lockdown (dager)    Antall ventilatorer
--------------------------------  ---------------------
                              29                678.955
                              30                817.75

   Vi kan konkludere med at hadde lockdown blitt innført fire dager senere, ville antallet 
   smittede ha blitt dobelt og helsevesenet ville ha blitt overveldet.                                        
   '''