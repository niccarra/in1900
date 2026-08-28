''' 
Opprinelig kode for å summere 1/2*k**2 for k=0,1,2,...,M
s = 0
M = 3
for i in range(M):
    s += 1/2*k**2 
print(s)

1. range(M) gir en liste med tallene 0,1,2,...,M-1; men vi vil ha 1,2,...,M. Derfor må vi endre range(M) til range(1,M+1).
2. Variabelen k er ikke definert i koden. Vi må endre k til i i summen, slik at det blir s += 1/2*i**2.
3. Nevneren burde være 2 ganger k, begge opphøyd i k-te potens. Derfor må vi endre 1/2*k**2 til 1/(2*i)**2.
'''

# Rettet kode for å summere 1/(2*k)**2 for k=1,2,...,M
s = 0
M = 3
for i in range(1, M + 1):
    s += 1/(2*i)**2
print(s)

# Vi kan verifisere at summen er korrekt ved å sammenligne med den analytiske løsningen for summen av 1/(2*k)**2 for k=1,2,...,M. Den analytiske løsningen er gitt ved formelen:
# S = 1/(2*1)**2 + 1/(2*2)**2 + 1/(2*3)**2 = 1/4 + 1/16 + 1/36
print(s == 1/4 + 1/16 + 1/36)  # Dette skal returnere True hvis summen er korrekt