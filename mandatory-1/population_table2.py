from population_table import population_growth
import numpy as np

start = 0
end = 48
num_samples = 12
t_samples = np.linspace(start, end, num = num_samples + 1)
N_samples = population_growth(50000, 9, 0.2, t_samples)

tN1 = [t_samples, N_samples]
'''
 La oss sjekke at lengden av tN1 er 2
Jeg valgte å bruke np.shape for å sjekke lengden av tN1 her
np.shape(A)[0] tilsvarer len[A]
np.shape(A)[1] tilsvarer len[A[0]]
'''
print("Length of tN1:", np.shape(tN1)[0])

### Skriv ut tabellen med t og N(t) i to kolonner
print("Time (hours) | Population")
print("")
for i in range(np.shape(tN1)[1]):
    print(f"{tN1[0][i]:12.0f} | {tN1[1][i]:8.0f}") 

tN2 = []
for i in range(len(t_samples)):
    tN2.append((t_samples[i], N_samples[i]))
### La oss sjekke at lengden av tN2 er den samme som lengden av t_samples
print("Har tN2 og t_samples samme lengde?", np.shape(tN2)[0] == len(t_samples))

### Skriv ut tabellen med t og N(t) i to kolonner
print("Time (hours) | Population")
print("")
for i in range(np.shape(tN2)[0]):
    print(f"{tN2[i][0]:12.0f} | {tN2[i][1]:8.0f}") 