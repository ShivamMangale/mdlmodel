import numpy as np
import random

new = np.random.uniform(low=-1e-1, high=1e-2, size=(1,11))
print(new)
for l in range(11):
    ind = 0
    chpow = 0
    # print(chpow)
    while abs(new[0][l]/pow(10,-chpow)) < 1:
        chpow += 1
        # print(new[0][l])
    print(chpow)
    new[0][l] += random.random()*random.randrange(-10,10)/pow(10,-chpow+1)
    new[0][l] = max(new[0][l],-10)
    new[0][l] = min(new[0][l],10)

print(new)