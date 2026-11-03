'''
Problem 3.5. Sum as a while loop Write the (corrected) for loop from the
previous exercise as a a while loop. Check that the two loops compute the same
answer
'''

i = 0
s = 0
M = 3

# Vi bruker walrus operator for å være fancy
while (i := i+1) <= M:
    s += 1/(2*i)**2

print(s)  

'''
Vi kan verifisere at summen er korrekt i det samme måte som i for-løkken
s må være lik 1/4 + 1/16 + 1/36
'''
print(s == 1/4 + 1/16 + 1/36)  # Dette skal returnere True hvis summen er korrekt