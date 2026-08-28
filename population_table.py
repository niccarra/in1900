import numpy as np
from tabulate import tabulate

'''
Ligning fra oppgave 2.3

'''
def population_growth(B, C, k, t):
    '''
    Return the number of individuals in a population at time t, given the parameters B, C, and k.
    B: carrying capacity
    C: constant related to initial population size
    k: growth rate constant
    t: time in hours
    '''
    return B / (1 + C * np.exp(-k * t))

'''
Vi må først finne verdiene for C når:
B = 50000
N_0 = 5000
k = 0.2

Ligningen for C er gitt ved:
N_0 = B / (1 + C * exp(-k * 0)) 
5000 = 50000 / (1 + C * 1)
5000 * (1 + C) = 50000
5000 + 5000 * C = 50000
5000 * C = 50000 - 5000
C = (50000 - 5000) / 5000
C = 9
'''


start = 0
end = 48
t_samples = np.linspace(start, end, num = 12,)
N_samples = population_growth(50000, 9, 0.2, t_samples)

table = list(zip(t_samples, N_samples))
tabulated_table = tabulate(table, headers=["Time (hours)", "Population"])
print(tabulated_table)

'''Problemformulering ber oss å bruke en for-løkke. La oss gjøre det da'''
N_samples = []
for t in t_samples:
    N_samples.append(population_growth(50000, 9, 0.2, t))
print("Time (hours) | Population")
print("")
for i in range(len(t_samples)):
    print(f"{t_samples[i]:12.2f} | {N_samples[i]:8.2f}")    
